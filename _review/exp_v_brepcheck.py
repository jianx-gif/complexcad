# -*- coding: utf-8 -*-
"""实验V: 用 BRepCheck_Analyzer 做真正的 B-rep 有效性审计 (批注 p44 #126).

第5章原来的"有效"只等于"执行后得到非空实体"——导师批评这个判据太弱.
本实验对每个已释出的 model.brep 跑 OCCT 自带的完整拓扑/几何检查:
  * BRepCheck_Analyzer(shape, True).IsValid()  —— 逐子形状检查(自交除外的全部规则)
  * 另外记录: 壳是否闭合 (BRepCheck_Shell), 体积/面积是否为正,
    最大面容差 (sliver/tolerance 异常的代理指标), 最小边长.
输出: _review/exp_v_brepcheck.json + _records.jsonl
用法: python exp_v_brepcheck.py [n]   (默认全部)
"""
import sys, os, json, math, collections

ROOT = r'E:/3005/data'
OUT = os.path.join(ROOT, 'output')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 0

from OCP.BRep import BRep_Builder, BRep_Tool
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_SHELL
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.GCPnts import GCPnts_AbscissaPoint
from OCP.BRepAdaptor import BRepAdaptor_Curve


def check(uuid):
    p = os.path.join(OUT, uuid, 'model.brep')
    if not os.path.isfile(p):
        return None
    shape = TopoDS_Shape()
    if not BRepTools.Read_s(shape, p, BRep_Builder()):
        return dict(uuid=uuid, error='read')
    rec = dict(uuid=uuid)
    try:
        rec['valid'] = bool(BRepCheck_Analyzer(shape, True).IsValid())
    except Exception as e:
        return dict(uuid=uuid, error='analyzer:' + str(e)[:50])
    # closed shells
    n_shell = n_closed = 0
    ex = TopExp_Explorer(shape, TopAbs_SHELL)
    while ex.More():
        sh = TopoDS.Shell_s(ex.Current())
        n_shell += 1
        if sh.Closed():
            n_closed += 1
        ex.Next()
    rec['shells'], rec['closed_shells'] = n_shell, n_closed
    # volume / area
    gp = GProp_GProps(); BRepGProp.VolumeProperties_s(shape, gp); vol = gp.Mass()
    ga = GProp_GProps(); BRepGProp.SurfaceProperties_s(shape, ga); area = ga.Mass()
    rec['volume'] = round(vol, 6); rec['area'] = round(area, 6)
    # tolerances and slivers
    tmax = 0.0; n_face = 0
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current())
        tmax = max(tmax, BRep_Tool.Tolerance_s(f))
        n_face += 1
        ex.Next()
    emin = float('inf'); n_edge = 0; n_tiny = 0
    ex = TopExp_Explorer(shape, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge_s(ex.Current())
        if BRep_Tool.Degenerated_s(e):      # 锥/球顶点的退化边, 长度天然为 0
            ex.Next(); continue
        try:
            L = GCPnts_AbscissaPoint.Length_s(BRepAdaptor_Curve(e))
            if L < emin:
                emin = L
            if L < 1e-3:
                n_tiny += 1
        except Exception:
            pass
        n_edge += 1
        ex.Next()
    rec.update(faces=n_face, edges=n_edge, max_face_tol=round(tmax, 9),
               min_edge_len=(round(emin, 6) if math.isfinite(emin) else None),
               tiny_edges=n_tiny)
    return rec


if __name__ == '__main__':
    uuids = sorted(u for u in os.listdir(OUT) if os.path.isfile(os.path.join(OUT, u, 'model.brep')))
    if N:
        uuids = uuids[:N]
    fo = open(os.path.join(ROOT, '_review', 'exp_v_brepcheck_records.jsonl'), 'w', encoding='utf-8')
    recs = []
    for i, u in enumerate(uuids, 1):
        try:
            r = check(u)
        except Exception as e:
            r = dict(uuid=u, error='fatal:' + str(e)[:60])
        if r:
            recs.append(r); fo.write(json.dumps(r) + '\n')
        if i % 500 == 0:
            print(i, '/', len(uuids), flush=True)
    fo.close()
    ok = [r for r in recs if 'error' not in r]
    n = max(1, len(ok))
    valid = sum(1 for r in ok if r['valid'])
    closed = sum(1 for r in ok if r['shells'] and r['closed_shells'] == r['shells'])
    posvol = sum(1 for r in ok if r['volume'] > 0)
    tiny = sum(1 for r in ok if r['tiny_edges'] > 0)
    hitol = sum(1 for r in ok if r['max_face_tol'] > 1e-6)
    summary = dict(n_models=len(ok), n_errors=len(recs) - len(ok),
                   brepcheck_valid=valid, brepcheck_valid_rate=round(valid / n, 4),
                   all_shells_closed=closed, all_shells_closed_rate=round(closed / n, 4),
                   positive_volume=posvol, positive_volume_rate=round(posvol / n, 4),
                   models_with_tiny_edges=tiny, tiny_edge_rate=round(tiny / n, 4),
                   models_with_face_tol_above_1e6=hitol, face_tol_rate=round(hitol / n, 4),
                   max_face_tol_seen=max((r['max_face_tol'] for r in ok), default=None),
                   min_edge_len_seen=min((r['min_edge_len'] for r in ok if r['min_edge_len'] is not None), default=None))
    json.dump(summary, open(os.path.join(ROOT, '_review', 'exp_v_brepcheck.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))
