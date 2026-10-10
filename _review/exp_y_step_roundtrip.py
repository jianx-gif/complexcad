# -*- coding: utf-8 -*-
"""实验Y: 全量 STEP 往返 (审计发现: "外形尺寸往返无损" 此前只在 3 个真实模型 + 9 个合成立方体上测过).

对每个已释出的 model.brep:
   读入 -> STEPControl_Writer 写 STEP (AP214, 单位 mm) -> STEPControl_Reader 读回
   比较: 包围盒 6 个坐标的最大绝对偏差 (mm), 以及 F/E/V 计数是否不变.
报告: 最大偏差、偏差分布、计数不变率、失败数.
用法 (cadquery 环境): python exp_y_step_roundtrip.py [n]
输出: _review/exp_y_step_roundtrip.json + _records.jsonl
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import sys, os, json, tempfile, io, contextlib

ROOT = _ROOT
OUT = os.path.join(ROOT, 'output')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 0

from OCP.BRep import BRep_Builder
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape
from OCP.STEPControl import STEPControl_Writer, STEPControl_Reader, STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone
from OCP.Interface import Interface_Static
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.TopExp import TopExp
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCP.TopTools import TopTools_IndexedMapOfShape

Interface_Static.SetCVal_s('write.step.unit', 'MM')
Interface_Static.SetCVal_s('write.step.schema', 'AP214IS')


def bbox(s):
    b = Bnd_Box(); b.SetGap(0.0); BRepBndLib.AddOptimal_s(s, b, False, False)
    return b.Get()


def fev(s):
    out = []
    for t in (TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX):
        m = TopTools_IndexedMapOfShape(); TopExp.MapShapes_s(s, t, m); out.append(m.Extent())
    return out


def roundtrip(uuid, tmp):
    s = TopoDS_Shape()
    if not BRepTools.Read_s(s, os.path.join(OUT, uuid, 'model.brep'), BRep_Builder()):
        return dict(uuid=uuid, error='brep-read')
    p = os.path.join(tmp, 'rt.step')
    with contextlib.redirect_stdout(io.StringIO()):
        w = STEPControl_Writer()
        w.Transfer(s, STEPControl_AsIs)
        if w.Write(p) != IFSelect_RetDone:
            return dict(uuid=uuid, error='step-write')
        r = STEPControl_Reader()
        if r.ReadFile(p) != IFSelect_RetDone:
            return dict(uuid=uuid, error='step-read')
        r.TransferRoots()
        s2 = r.OneShape()
    b1, b2 = bbox(s), bbox(s2)
    dev = max(abs(x - y) for x, y in zip(b1, b2))
    c1, c2 = fev(s), fev(s2)
    ext = max(b1[3] - b1[0], b1[4] - b1[1], b1[5] - b1[2])
    return dict(uuid=uuid, bbox_dev_mm=dev, extent_mm=round(ext, 4), fev_before=c1, fev_after=c2,
                fev_same=c1 == c2)


if __name__ == '__main__':
    uuids = sorted(u for u in os.listdir(OUT) if os.path.isfile(os.path.join(OUT, u, 'model.brep')))
    if N:
        uuids = uuids[:N]
    tmp = tempfile.mkdtemp(prefix='rt_')
    rec_path = os.path.join(ROOT, '_review', 'exp_y_step_roundtrip_records.jsonl')
    marker = os.path.join(ROOT, '_review', 'exp_y_current.txt')
    done = {}
    if os.path.isfile(rec_path):
        for l in open(rec_path, encoding='utf-8'):
            try:
                r = json.loads(l); done[r['uuid']] = r
            except Exception:
                pass
    fo = open(rec_path, 'a', encoding='utf-8')
    for i, u in enumerate(uuids, 1):
        if u in done:
            continue
        open(marker, 'w').write(u)
        try:
            r = roundtrip(u, tmp)
        except Exception as e:
            r = dict(uuid=u, error='fatal:' + str(e)[:60])
        done[u] = r; fo.write(json.dumps(r) + '\n'); fo.flush()
        if i % 500 == 0:
            print(i, '/', len(uuids), flush=True)
    fo.close()
    if os.path.isfile(marker):
        os.remove(marker)
    recs = [done[u] for u in uuids if u in done]
    ok = [r for r in recs if 'error' not in r]
    devs = sorted(r['bbox_dev_mm'] for r in ok)
    n = max(1, len(ok))

    def q(p):
        return devs[min(len(devs) - 1, int(p * len(devs)))] if devs else None
    summary = dict(n_models=len(recs), n_ok=len(ok), n_errors=len(recs) - len(ok),
                   bbox_dev_max_mm=devs[-1] if devs else None, bbox_dev_median_mm=q(0.5),
                   bbox_dev_p99_mm=q(0.99),
                   within_1e_9=sum(1 for d in devs if d <= 1e-9), within_1e_6=sum(1 for d in devs if d <= 1e-6),
                   within_1e_3=sum(1 for d in devs if d <= 1e-3),
                   fev_unchanged=sum(1 for r in ok if r['fev_same']),
                   fev_unchanged_rate=round(sum(1 for r in ok if r['fev_same']) / n, 4))
    json.dump(summary, open(os.path.join(ROOT, '_review', 'exp_y_step_roundtrip.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))
