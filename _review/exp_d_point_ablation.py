# -*- coding: utf-8 -*-
"""实验D: 点数消融 1024/2048/4096/8192 (批注p25).
采样为网格面积均匀 -> 每个B-rep面被采到的概率有解析闭式:
  P(face covered) = 1 - (1 - A_f/A_total)^N
1) 解析部分: 对含 fillet 具名参数的分层样本, 识别 fillet 面(圆柱/环面, 半径==具名
   fillet 参数), 报告 fillet 表面覆盖概率随 N 的分布; 另报小面(面积P10以下)覆盖.
2) 实测部分: 30件 x 5种子 x 4档N, trimesh 采样验证三角形级覆盖与解析预测吻合.
用法: python exp_d_point_ablation.py <n_models>
"""
import sys, os, json, glob, re, random
import numpy as np

ROOT = r'E:/3005/data'
N_MODELS = int(sys.argv[1]) if len(sys.argv) > 1 else 300
NS = [1024, 2048, 4096, 8192]
PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)

from OCP.BRep import BRep_Builder
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Torus

def faces_of(path):
    shape = TopoDS_Shape()
    b = BRep_Builder()
    if not BRepTools.Read_s(shape, path, b):
        return None
    out = []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current())
        props = GProp_GProps()
        BRepGProp.SurfaceProperties_s(f, props)
        area = props.Mass()
        ad = BRepAdaptor_Surface(f)
        t = ad.GetType()
        r = None
        if t == GeomAbs_Cylinder:
            r = ad.Cylinder().Radius()
        elif t == GeomAbs_Torus:
            r = ad.Torus().MinorRadius()
        out.append((area, r))
        ex.Next()
    return out

# 样本: 含 fillet 具名参数的模型
random.seed(42)
cands = []
for py in glob.glob(os.path.join(ROOT, 'output', '*', 'cadquery.py')):
    src = open(py, encoding='utf-8', errors='replace').read()
    fr = [float(v) for nm, v in PARAM_RE.findall(src) if 'fillet' in nm.lower() and float(v) > 0]
    if fr:
        cands.append((os.path.dirname(py), fr))
random.shuffle(cands)
cands = cands[:N_MODELS]
print('fillet-param models sampled:', len(cands), flush=True)

cov = {N: [] for N in NS}          # 每模型 fillet 表面覆盖概率
small_cov = {N: [] for N in NS}    # 每模型 最小面 覆盖概率
frac_area = []
matched = 0
for i, (d, frads) in enumerate(cands):
    fl = faces_of(os.path.join(d, 'model.brep'))
    if not fl:
        continue
    total = sum(a for a, _ in fl)
    fil = [a for a, r in fl if r is not None and any(abs(r - x) < 1e-6 for x in frads)]
    amin = min(a for a, _ in fl)
    for N in NS:
        small_cov[N].append(1 - (1 - amin / total) ** N)
    if fil:
        matched += 1
        af = sum(fil)
        frac_area.append(af / total)
        for N in NS:
            cov[N].append(1 - (1 - af / total) ** N)
    if (i + 1) % 50 == 0:
        print('...', i + 1, flush=True)

def stats(xs):
    xs = np.array(xs)
    return {'median': round(float(np.median(xs)), 4),
            'p5': round(float(np.quantile(xs, 0.05)), 4),
            'min': round(float(xs.min()), 4)}

res = {'n_models': len(cands), 'n_with_matched_fillet_faces': matched,
       'fillet_area_fraction_median': round(float(np.median(frac_area)), 4),
       'fillet_surface_coverage': {N: stats(cov[N]) for N in NS},
       'smallest_face_coverage': {N: stats(small_cov[N]) for N in NS}}

# 实测: 30件 x 5种子, 三角形覆盖与解析比对
import trimesh
emp_err = []
for d, _ in cands[:30]:
    m = trimesh.load(os.path.join(d, 'model.stl'), force='mesh')
    A = m.area_faces
    tot = A.sum()
    for N in (1024, 8192):
        ana = 1 - (1 - A / tot) ** N
        hits = np.zeros((5, len(A)), bool)
        for s in range(5):
            _, fid = trimesh.sample.sample_surface(m, N, seed=s)
            hits[s, np.unique(fid)] = True
        emp = hits.mean(0)
        emp_err.append(float(np.abs(emp - ana).mean()))
res['empirical_vs_analytic_mean_abs_err'] = round(float(np.mean(emp_err)), 4)

print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(ROOT, '_review', 'exp_d_point_ablation.json'), 'w'), indent=1)
