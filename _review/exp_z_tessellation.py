# -*- coding: utf-8 -*-
"""实验Z: 继承的 STL 三角化相对精确 B-rep 曲面的弦高偏差 (批注 p24/p25 #78/#82).

点云是从上游 STL 采样的, 本流水线没设三角化容差. 这里实测这张网格离真实曲面有多远:
对 seed 42 抽 60 个模型, 每个按面积加权取 300 个三角形, 在三角形重心处
(三角化误差最大的位置之一) 用 BRepExtrema 求到 model.brep 的距离.
报告: 每模型最大偏差的中位数/P95/最大值 (mm), 以及相对包围盒对角线的比例.
用法 (cadfit-env: 有 OCP + trimesh): python exp_z_tessellation.py
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, json, random, glob
import numpy as np
import trimesh
from OCP.BRep import BRep_Builder
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCP.gp import gp_Pnt
from OCP.BRepExtrema import BRepExtrema_DistShapeShape

R = _ROOT
rows = [json.loads(l) for l in open(os.path.join(R, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8')]
pool = sorted(r['uuid'] for r in rows if r.get('valid'))
random.seed(42)
sample = random.sample(pool, 60)
per_model = []
for u in sample:
    d = os.path.join(R, 'output', u)
    m = trimesh.load(os.path.join(d, 'model.stl'), force='mesh')
    s = TopoDS_Shape()
    if not BRepTools.Read_s(s, os.path.join(d, 'model.brep'), BRep_Builder()):
        continue
    rng = np.random.default_rng(0)
    idx = rng.choice(len(m.faces), size=min(300, len(m.faces)), replace=False, p=m.area_faces / m.area_faces.sum())
    cents = m.triangles_center[idx]
    dmax = 0.0
    for c in cents:
        v = BRepBuilderAPI_MakeVertex(gp_Pnt(float(c[0]), float(c[1]), float(c[2]))).Vertex()
        ext = BRepExtrema_DistShapeShape(v, s)
        if ext.IsDone():
            dmax = max(dmax, ext.Value())
    diag = float(np.linalg.norm(m.bounds[1] - m.bounds[0]))
    per_model.append(dict(uuid=u, max_dev_mm=dmax, diag_mm=diag, triangles=len(m.faces)))
dev = np.array([p['max_dev_mm'] for p in per_model])
rel = np.array([p['max_dev_mm'] / p['diag_mm'] for p in per_model])
out = dict(n_models=len(per_model), points_per_model=300,
           max_dev_mm=dict(median=round(float(np.median(dev)), 5), p95=round(float(np.quantile(dev, .95)), 5),
                           max=round(float(dev.max()), 5)),
           max_dev_rel_to_diag=dict(median=float(np.median(rel)), max=float(rel.max())),
           triangles_median=int(np.median([p['triangles'] for p in per_model])))
json.dump(dict(summary=out, models=per_model), open(os.path.join(R, '_review', 'exp_z_tessellation.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
