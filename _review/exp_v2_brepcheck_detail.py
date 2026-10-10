# -*- coding: utf-8 -*-
"""实验V2: (a) 61 个 BRepCheck 不合格的 B-rep 按"哪类子形状、哪种检查失败"分类, 并统计其中含哪些操作;
(b) 全部 9980 个释出 B-rep 的最大 面/边/顶点 容差 (批注 #86: 记录每个形状实际存储的容差).
用法 (cadquery 环境): python exp_v2_brepcheck_detail.py
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, json, collections
from OCP.BRep import BRep_Builder, BRep_Tool
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHELL, TopAbs_WIRE
from OCP.BRepCheck import BRepCheck_Analyzer, BRepCheck_NoError

R = _ROOT
OUT = os.path.join(R, 'output')
invalid = set(json.load(open(os.path.join(R, '_review', 'brepcheck_invalid.json')))['uuids'])
metrics = {json.loads(l)['uuid']: json.loads(l) for l in open(os.path.join(R, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8')}


def read(u):
    s = TopoDS_Shape()
    BRepTools.Read_s(s, os.path.join(OUT, u, 'model.brep'), BRep_Builder())
    return s


def status_names(res):
    names = []
    try:
        for st in res.Status():
            if st != BRepCheck_NoError:
                names.append(str(st).split('.')[-1])
    except Exception:
        pass
    return names


kinds = collections.Counter(); stat = collections.Counter(); ops = collections.Counter()
per_model = {}
for u in sorted(invalid):
    s = read(u)
    an = BRepCheck_Analyzer(s, True)
    bad = collections.Counter()
    for typ, lab in ((TopAbs_SHELL, 'shell'), (TopAbs_FACE, 'face'), (TopAbs_WIRE, 'wire'), (TopAbs_EDGE, 'edge'), (TopAbs_VERTEX, 'vertex')):
        ex = TopExp_Explorer(s, typ)
        while ex.More():
            sub = ex.Current()
            try:
                ok = an.IsValid(sub)
            except Exception:
                ok = True
            if not ok:
                bad[lab] += 1
                try:
                    for n in status_names(an.Result(sub)):
                        stat[n] += 1
                except Exception:
                    pass
            ex.Next()
    first = next((k for k in ('shell', 'face', 'wire', 'edge', 'vertex') if bad[k]), 'solid-level')
    kinds[first] += 1
    for o in set(x.lower() for x in (metrics.get(u, {}).get('ops') or [])):
        ops[o] += 1
    per_model[u] = dict(bad=dict(bad), first=first)

# (b) stored tolerances over all released B-reps
tmax = {'face': 0.0, 'edge': 0.0, 'vertex': 0.0}
over = {'edge_1e-4': 0, 'vertex_1e-4': 0, 'edge_1e-3': 0, 'vertex_1e-3': 0}
n = 0
for u in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, u, 'model.brep')
    if not os.path.isfile(p):
        continue
    s = read(u); n += 1
    mm = {'face': 0.0, 'edge': 0.0, 'vertex': 0.0}
    for typ, lab, f in ((TopAbs_FACE, 'face', lambda x: BRep_Tool.Tolerance_s(TopoDS.Face_s(x))),
                        (TopAbs_EDGE, 'edge', lambda x: BRep_Tool.Tolerance_s(TopoDS.Edge_s(x))),
                        (TopAbs_VERTEX, 'vertex', lambda x: BRep_Tool.Tolerance_s(TopoDS.Vertex_s(x)))):
        ex = TopExp_Explorer(s, typ)
        while ex.More():
            mm[lab] = max(mm[lab], f(ex.Current())); ex.Next()
    for k in tmax:
        tmax[k] = max(tmax[k], mm[k])
    over['edge_1e-4'] += mm['edge'] > 1e-4; over['vertex_1e-4'] += mm['vertex'] > 1e-4
    over['edge_1e-3'] += mm['edge'] > 1e-3; over['vertex_1e-3'] += mm['vertex'] > 1e-3
res = dict(n_invalid=len(invalid), first_failing_level=dict(kinds), status_counts=dict(stat.most_common(12)),
           operations_in_invalid=dict(ops.most_common(12)),
           tolerances=dict(n_models=n, max_mm=tmax, models_above=over))
json.dump(dict(summary=res, per_model=per_model), open(os.path.join(R, '_review', 'exp_v2_brepcheck_detail.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
