# -*- coding: utf-8 -*-
"""实验G: 逐操作几何测量器 (批注p45).
从 model.brep 实测特征尺寸, 与源码具名参数对照:
  diameter 类  <-> 圆柱面直径 2r
  fillet 类    <-> 圆柱/环面半径 r
  chamfer 类   <-> 平面倒角带最小延展 / sqrt(2)
  depth 类     <-> 圆柱面轴向延展
报告 attempted / exact(<=1e-6) / close(<=0.01mm) / unmatched + 残差分布.
用法: python exp_g_measurers.py <n_models>
"""
import sys, os, json, glob, re, random, math
import numpy as np

ROOT = r'E:/3005/data'
N_MODELS = int(sys.argv[1]) if len(sys.argv) > 1 else 600
PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)

from OCP.BRep import BRep_Builder
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Torus, GeomAbs_Plane

def features(path):
    shape = TopoDS_Shape()
    if not BRepTools.Read_s(shape, path, BRep_Builder()):
        return None
    cyl_r, cyl_h, tor_r, plane_minext = [], [], [], []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current())
        ad = BRepAdaptor_Surface(f)
        t = ad.GetType()
        u0, u1, v0, v1 = ad.FirstUParameter(), ad.LastUParameter(), ad.FirstVParameter(), ad.LastVParameter()
        if t == GeomAbs_Cylinder:
            r = ad.Cylinder().Radius()
            cyl_r.append(r)
            if all(map(math.isfinite, (v0, v1))):
                cyl_h.append(abs(v1 - v0))          # 圆柱V参数=轴向长度
        elif t == GeomAbs_Torus:
            tor_r.append(ad.Torus().MinorRadius())
        elif t == GeomAbs_Plane:
            if all(map(math.isfinite, (u0, u1, v0, v1))):
                plane_minext.append(min(abs(u1 - u0), abs(v1 - v0)))
        ex.Next()
    return cyl_r, cyl_h, tor_r, plane_minext

def classify(name):
    low = name.lower()
    if 'fillet' in low:
        return 'fillet'
    if 'chamfer' in low:
        return 'chamfer'
    if 'dia' in low or 'bore' in low:
        return 'diameter'
    if 'depth' in low:
        return 'depth'
    return None

random.seed(42)
dirs = sorted(glob.glob(os.path.join(ROOT, 'output', '*')))
random.shuffle(dirs)

stats = {k: {'attempted': 0, 'exact': 0, 'close': 0, 'unmatched': 0, 'errs': []}
         for k in ('diameter', 'fillet', 'chamfer', 'depth')}
n_used = 0
for d in dirs:
    if n_used >= N_MODELS:
        break
    py = os.path.join(d, 'cadquery.py')
    br = os.path.join(d, 'model.brep')
    if not (os.path.isfile(py) and os.path.isfile(br)):
        continue
    src = open(py, encoding='utf-8', errors='replace').read()
    params = [(nm, float(v)) for nm, v in PARAM_RE.findall(src)]
    params = [(nm, v, classify(nm)) for nm, v in params]
    params = [(nm, v, c) for nm, v, c in params if c and v > 0]
    if not params:
        continue
    fl = features(br)
    if fl is None:
        continue
    cyl_r, cyl_h, tor_r, plane_minext = fl
    n_used += 1
    for nm, v, c in params:
        st = stats[c]
        st['attempted'] += 1
        if c == 'diameter':
            cand = [2 * r for r in cyl_r]
        elif c == 'fillet':
            cand = cyl_r + tor_r
        elif c == 'depth':
            cand = cyl_h
        else:  # chamfer: 带宽 = sqrt(2)*c (等距45度)
            cand = [w / math.sqrt(2) for w in plane_minext]
        if not cand:
            st['unmatched'] += 1
            continue
        err = min(abs(x - v) for x in cand)
        st['errs'].append(err)
        if err <= 1e-6:
            st['exact'] += 1
        elif err <= 0.01:
            st['close'] += 1

out = {'n_models': n_used}
for k, st in stats.items():
    errs = np.array(st['errs']) if st['errs'] else np.array([np.nan])
    matched = st['exact'] + st['close']
    out[k] = {
        'attempted': st['attempted'],
        'exact_1e-6': st['exact'],
        'close_0.01mm': st['close'],
        'no_candidate_feature': st['unmatched'],
        'match_rate': round(matched / max(1, st['attempted']), 4),
        'median_err_mm': round(float(np.nanmedian(errs)), 6),
        'p95_err_mm': round(float(np.nanquantile(errs, 0.95)), 4),
    }
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(ROOT, '_review', 'exp_g_measurers.json'), 'w'), indent=1)
