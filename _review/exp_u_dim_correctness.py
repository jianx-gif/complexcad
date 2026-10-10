# -*- coding: utf-8 -*-
"""实验U: 工程图尺寸「数值正确率」审计 (批注 p31 #92/#93 尚缺的两项).

实验T 只做了 参数 -> 图纸 的覆盖率(召回). 本实验做反方向(精度):
图上每一条尺寸文字, 其数值能否归因到
  (a) 源程序里的具名参数, 或
  (b) 从 model.brep 实测的几何量:
        ⌀v  -> 某圆柱面直径 2r 或某圆边直径 2r
        Rv  -> 某圆柱/圆环/圆边半径 r
        v   -> 包围盒三个尺寸, 或某圆柱轴向长度, 或平面面片的 U/V 延展
        Cv  -> 倒角带最小延展 / sqrt(2) (与 exp_g 同口径)
        v°  -> 只对参数比对(角度不在面上直接可测)
两者都对不上的记为 unattributable —— 这是「错误/多余尺寸率」的上界.
另外单列 错标⌀率 / 错标R率: ⌀(或R)尺寸找不到任何相容圆特征.

用法: python exp_u_dim_correctness.py [n_models]   (默认 600, 与 exp_g 同样本量, seed 42)
输出: _review/exp_u_dim_correctness.json + _records.jsonl
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import sys, os, re, json, math, random, collections

ROOT = _ROOT
OUT = os.path.join(ROOT, 'output')
N_MODELS = int(sys.argv[1]) if len(sys.argv) > 1 else 600
TOL_REL, TOL_ABS = 1e-3, 0.01

import ezdxf
from OCP.BRep import BRep_Builder
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Torus, GeomAbs_Plane, GeomAbs_Cone, GeomAbs_Circle
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)
DIM_RE = re.compile(r"^(?:(\d+)x\s*)?([\u2300\u00d8RCM]?)\s*(-?\d+\.?\d*)\s*(\u00b0)?$")


def parse_dim(text):
    t = text.strip().replace('\u00d8', '\u2300')
    m = DIM_RE.match(t)
    if not m:
        return None
    mult, pre, val, deg = m.groups()
    kind = 'angle' if deg else {'\u2300': 'diameter', 'R': 'radius', 'C': 'chamfer', 'M': 'thread'}.get(pre, 'linear')
    return kind, float(val), int(mult) if mult else 1


def measure(brep_path):
    """实测量集合: 直径候选 / 半径候选 / 线性候选 / 倒角候选."""
    shape = TopoDS_Shape()
    if not BRepTools.Read_s(shape, brep_path, BRep_Builder()):
        return None
    radii, linear, chamfer = set(), set(), set()
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current())
        ad = BRepAdaptor_Surface(f)
        t = ad.GetType()
        u0, u1, v0, v1 = ad.FirstUParameter(), ad.LastUParameter(), ad.FirstVParameter(), ad.LastVParameter()
        if t == GeomAbs_Cylinder:
            radii.add(round(ad.Cylinder().Radius(), 4))
            if math.isfinite(v0) and math.isfinite(v1):
                linear.add(round(abs(v1 - v0), 4))
        elif t == GeomAbs_Torus:
            radii.add(round(ad.Torus().MinorRadius(), 4))
            radii.add(round(ad.Torus().MajorRadius(), 4))
        elif t == GeomAbs_Cone:
            # 倒角常以圆锥面出现: 用锥面沿轴的斜宽 * cos(半角) 作倒角距离候选
            try:
                ang = ad.Cone().SemiAngle()
                if math.isfinite(v0) and math.isfinite(v1):
                    slant = abs(v1 - v0)
                    chamfer.add(round(abs(slant * math.cos(ang)), 4))
                    chamfer.add(round(abs(slant * math.sin(ang)), 4))
            except Exception:
                pass
        elif t == GeomAbs_Plane:
            if all(map(math.isfinite, (u0, u1, v0, v1))):
                du, dv = abs(u1 - u0), abs(v1 - v0)
                linear.add(round(du, 4)); linear.add(round(dv, 4))
                chamfer.add(round(min(du, dv) / math.sqrt(2), 4))
        ex.Next()
    ex = TopExp_Explorer(shape, TopAbs_EDGE)
    n_edge = 0
    while ex.More() and n_edge < 4000:
        e = TopoDS.Edge_s(ex.Current())
        try:
            ac = BRepAdaptor_Curve(e)
            if ac.GetType() == GeomAbs_Circle:
                radii.add(round(ac.Circle().Radius(), 4))
        except Exception:
            pass
        n_edge += 1
        ex.Next()
    b = Bnd_Box(); BRepBndLib.Add_s(shape, b)
    xmin, ymin, zmin, xmax, ymax, zmax = b.Get()
    for d in (xmax - xmin, ymax - ymin, zmax - zmin):
        linear.add(round(d, 4))
    return dict(radii=radii, linear=linear, chamfer=chamfer)


def near(v, pool):
    tol = max(TOL_ABS, TOL_REL * abs(v))
    return any(abs(v - c) <= tol for c in pool)


def audit(uuid):
    d_dxf = os.path.join(OUT, uuid, 'drawing.dxf')
    d_py = os.path.join(OUT, uuid, 'cadquery.py')
    d_brep = os.path.join(OUT, uuid, 'model.brep')
    if not all(os.path.isfile(p) for p in (d_dxf, d_py, d_brep)):
        return None
    try:
        doc = ezdxf.readfile(d_dxf)
    except Exception as e:
        return dict(uuid=uuid, error='dxf:' + str(e)[:60])
    dims = []
    for e in doc.modelspace():
        if e.dxftype() == 'TEXT' and e.dxf.layer == 'DIM':
            p = parse_dim(e.dxf.text)
            if p:
                dims.append(p)
    if not dims:
        return dict(uuid=uuid, error='no-dims')
    params = {round(float(v), 4) for _, v in PARAM_RE.findall(open(d_py, encoding='utf-8', errors='replace').read())}
    try:
        g = measure(d_brep)
    except Exception as e:
        return dict(uuid=uuid, error='brep:' + str(e)[:60])
    if g is None:
        return dict(uuid=uuid, error='brep-read')
    diam_pool = {round(2 * r, 4) for r in g['radii']}
    rec = collections.Counter()
    per_kind = collections.defaultdict(lambda: [0, 0, 0, 0])   # [n, param, geom, either]
    for kind, v, mult in dims:
        rec['n'] += 1
        per_kind[kind][0] += 1
        p_ok = near(v, params)
        if kind == 'diameter':
            g_ok = near(v, diam_pool)
        elif kind == 'radius':
            g_ok = near(v, g['radii'])
        elif kind == 'linear':
            g_ok = near(v, g['linear']) or near(v, diam_pool) or near(v, g['radii'])
        elif kind == 'chamfer':
            g_ok = near(v, g['chamfer'])
        else:                                   # angle / thread: 几何侧不判定
            g_ok = False
        if p_ok:
            per_kind[kind][1] += 1; rec['param'] += 1
        if g_ok:
            per_kind[kind][2] += 1; rec['geom'] += 1
        if p_ok or g_ok:
            rec['attributable'] += 1
            per_kind[kind][3] += 1
        elif kind in ('angle', 'thread'):
            rec['angle_thread_unchecked'] += 1
        else:
            rec['unattributable'] += 1
            if kind == 'diameter':
                rec['bad_diameter'] += 1
            elif kind == 'radius':
                rec['bad_radius'] += 1
    return dict(uuid=uuid, counts=dict(rec), per_kind={k: v for k, v in per_kind.items()})


if __name__ == '__main__':
    uuids = sorted(u for u in os.listdir(OUT) if os.path.isfile(os.path.join(OUT, u, 'drawing.dxf')))
    random.seed(42); random.shuffle(uuids)
    uuids = uuids[:N_MODELS]
    recs = []
    fo = open(os.path.join(ROOT, '_review', 'exp_u_dim_correctness_records.jsonl'), 'w', encoding='utf-8')
    for i, u in enumerate(uuids, 1):
        try:
            r = audit(u)
        except Exception as e:
            r = dict(uuid=u, error='fatal:' + str(e)[:60])
        if r:
            recs.append(r); fo.write(json.dumps(r, ensure_ascii=False) + '\n'); fo.flush()
        if i % 50 == 0:
            print(i, '/', len(uuids), flush=True)
    fo.close()
    ok = [r for r in recs if 'error' not in r]
    tot = collections.Counter()
    kind_tot = collections.defaultdict(lambda: [0, 0, 0, 0])
    for r in ok:
        tot.update(r['counts'])
        for k, v in r['per_kind'].items():
            for idx in range(4): kind_tot[k][idx] += v[idx]
    n = max(1, tot['n'])
    checked = max(1, tot['n'] - tot.get('angle_thread_unchecked', 0))
    summary = dict(
        n_drawings=len(ok), n_errors=len(recs) - len(ok), n_dims=tot['n'],
        dims_per_drawing=round(tot['n'] / max(1, len(ok)), 2),
        matched_named_parameter=round(tot['param'] / n, 4),
        matched_measured_geometry=round(tot['geom'] / n, 4),
        attributable=round(tot['attributable'] / n, 4),
        unattributable_of_checkable=round(tot['unattributable'] / checked, 4),
        angle_thread_unchecked=tot.get('angle_thread_unchecked', 0),
        wrong_diameter_rate=round(tot.get('bad_diameter', 0) / max(1, kind_tot['diameter'][0]), 4),
        wrong_radius_rate=round(tot.get('bad_radius', 0) / max(1, kind_tot['radius'][0]), 4),
        by_kind={k: dict(n=v[0], param=round(v[1] / max(1, v[0]), 4), geom=round(v[2] / max(1, v[0]), 4),
                         neither=round((v[0] - v[3]) / max(1, v[0]), 4))
                 for k, v in kind_tot.items()},
        sample=dict(seed=42, n_requested=N_MODELS))
    json.dump(summary, open(os.path.join(ROOT, '_review', 'exp_u_dim_correctness.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))
