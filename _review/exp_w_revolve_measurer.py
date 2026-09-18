# -*- coding: utf-8 -*-
"""实验W: revolve 角度/轴 测量器 (批注 p45 #134/#136 里可做的一类).

对每个含 revolve 的模型:
  声明侧: 从 cadquery.py 解析 .revolve(...) 的角度实参
          (空 -> 默认 360; 数字字面量; 具名变量则从 params 解析)
  实测侧: 从 model.brep 取所有回转类曲面 (Cylinder / Cone / Torus / SurfaceOfRevolution)
          的 U 参数跨度(度), 取最大值作为该实体的回转角;
          同时记录这些面的轴方向, 检查是否共轴(轴一致性).
报告 attempted / matched(<=0.01 deg) / close(<=0.5 deg) / no-candidate + 误差分布,
并按 360 度 与 非 360 度 分开报, 因为完整回转是平凡情形.
用法: python exp_w_revolve_measurer.py [n]
输出: _review/exp_w_revolve.json + _records.jsonl
"""
import sys, os, re, json, math, collections

ROOT = r'E:/3005/data'
OUT = os.path.join(ROOT, 'output')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 0

from OCP.BRep import BRep_Builder
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import (GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Torus,
                         GeomAbs_SurfaceOfRevolution)

PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)
NUM = re.compile(r'^\s*(-?\d+(?:\.\d+)?)\s*(?:,|$)')
VAR = re.compile(r'^\s*([a-zA-Z_]\w*)\s*(?:,|$)')
REV = re.compile(r'\.revolve\(([^)]*)')


def declared_angles(src):
    params = {n: float(v) for n, v in PARAM_RE.findall(src)}
    out = []
    for m in REV.finditer(src):
        a = m.group(1).strip()
        if a == '':
            out.append(('default', 360.0))
        elif NUM.match(a):
            out.append(('literal', float(NUM.match(a).group(1))))
        elif VAR.match(a) and VAR.match(a).group(1) in params:
            out.append(('named', params[VAR.match(a).group(1)]))
        else:
            out.append(('unresolved', None))
    return out


def measured(brep_path):
    shape = TopoDS_Shape()
    if not BRepTools.Read_s(shape, brep_path, BRep_Builder()):
        return None
    spans, axes = [], []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current())
        ad = BRepAdaptor_Surface(f)
        t = ad.GetType()
        if t in (GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Torus, GeomAbs_SurfaceOfRevolution):
            u0, u1 = ad.FirstUParameter(), ad.LastUParameter()
            if math.isfinite(u0) and math.isfinite(u1):
                spans.append(math.degrees(abs(u1 - u0)))
            try:
                if t == GeomAbs_Cylinder:
                    d = ad.Cylinder().Axis().Direction()
                elif t == GeomAbs_Cone:
                    d = ad.Cone().Axis().Direction()
                elif t == GeomAbs_Torus:
                    d = ad.Torus().Axis().Direction()
                else:
                    d = ad.AxeOfRevolution().Direction()
                axes.append((round(d.X(), 5), round(d.Y(), 5), round(d.Z(), 5)))
            except Exception:
                pass
        ex.Next()
    return spans, axes


def coaxial(axes):
    """所有回转面是否同轴(方向平行, 允许反向)."""
    if not axes:
        return None
    a0 = axes[0]
    for a in axes[1:]:
        dot = abs(a0[0] * a[0] + a0[1] * a[1] + a0[2] * a[2])
        if dot < 0.999:
            return False
    return True


def run(uuid):
    py = os.path.join(OUT, uuid, 'cadquery.py')
    br = os.path.join(OUT, uuid, 'model.brep')
    if not (os.path.isfile(py) and os.path.isfile(br)):
        return None
    src = open(py, encoding='utf-8', errors='replace').read()
    decl = declared_angles(src)
    if not decl:
        return None
    m = measured(br)
    if m is None:
        return dict(uuid=uuid, error='brep')
    spans, axes = m
    rec = dict(uuid=uuid, n_calls=len(decl), n_rev_faces=len(spans),
               coaxial=coaxial(axes), results=[])
    for how, ang in decl:
        if ang is None:
            rec['results'].append(dict(how=how, declared=None, best=None, err=None))
            continue
        if not spans:
            rec['results'].append(dict(how=how, declared=ang, best=None, err=None))
            continue
        best = min(spans, key=lambda s: abs(s - ang))
        rec['results'].append(dict(how=how, declared=ang, best=round(best, 6),
                                   err=round(abs(best - ang), 6)))
    return rec


if __name__ == '__main__':
    metrics = os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl')
    uuids = [json.loads(l)['uuid'] for l in open(metrics, encoding='utf-8')
             if 'revolve' in (json.loads(l).get('ops') or [])]
    if N:
        uuids = uuids[:N]
    recs = []
    fo = open(os.path.join(ROOT, '_review', 'exp_w_revolve_records.jsonl'), 'w', encoding='utf-8')
    for i, u in enumerate(uuids, 1):
        try:
            r = run(u)
        except Exception as e:
            r = dict(uuid=u, error='fatal:' + str(e)[:60])
        if r:
            recs.append(r); fo.write(json.dumps(r) + '\n')
        if i % 200 == 0:
            print(i, '/', len(uuids), flush=True)
    fo.close()
    ok = [r for r in recs if 'error' not in r]
    buckets = collections.defaultdict(lambda: collections.Counter())
    errs = collections.defaultdict(list)
    for r in ok:
        for res in r['results']:
            grp = 'unresolved' if res['declared'] is None else ('full' if abs(res['declared'] - 360) < 1e-6 else 'partial')
            b = buckets[grp]
            b['attempted'] += 1
            if res['err'] is None:
                b['no_candidate'] += 1
                continue
            errs[grp].append(res['err'])
            if res['err'] <= 1e-2:
                b['exact'] += 1
            elif res['err'] <= 0.5:
                b['close'] += 1
            else:
                b['off'] += 1
    def med(v):
        v = sorted(v)
        return round(v[len(v) // 2], 6) if v else None
    coax = [r['coaxial'] for r in ok if r['coaxial'] is not None]
    summary = dict(n_models=len(ok), n_errors=len(recs) - len(ok),
                   by_group={g: dict(buckets[g], median_err_deg=med(errs[g])) for g in buckets},
                   coaxial_models=sum(1 for c in coax if c), coaxial_total=len(coax),
                   coaxial_rate=round(sum(1 for c in coax if c) / max(1, len(coax)), 4))
    json.dump(summary, open(os.path.join(ROOT, '_review', 'exp_w_revolve.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))
