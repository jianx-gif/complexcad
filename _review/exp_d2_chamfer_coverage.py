# -*- coding: utf-8 -*-
"""实验D2: 点数消融补全 (批注 p25 #85: 按 N 报 chamfer 与 fillet 覆盖, 并给最小特征尺寸).

与实验D同一口径 (面积均匀采样 -> 每个面被至少采到一点的概率 P = 1-(1-A_f/A)^N):
  * fillet 样本: 含具名 fillet 参数的模型, seed 42, 300 件 (与实验D 相同抽样)
  * chamfer 样本: 含具名 chamfer 参数的模型, seed 42, 300 件
    倒角面识别: 平面面片且 min(U,V 延展)/sqrt(2) == 具名 chamfer 值 (与实验G 测量器同口径),
               或圆锥面且 斜宽*cos/sin(半角) == 具名 chamfer 值 (圆边上的倒角)
报告: 每个 N 的 chamfer 表面覆盖 median/P5/min; 两样本的零件总面积中位数 (B-rep 实测);
      最小面面积 (mm2) 的中位数与 P5; 以及在 N=8192 下被覆盖概率 >=0.99 所需的最小面积占比
      与按中位面积换算的最小可靠特征面积.
用法 (cadquery 环境): python exp_d2_chamfer_coverage.py
输出: _review/exp_d2_chamfer_coverage.json
"""
import os, re, glob, json, math, random
import numpy as np

ROOT = r'E:/3005/data'
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
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cone


def near(v, pool):
    return any(abs(v - c) <= max(0.01, 1e-3 * abs(c)) for c in pool)


def faces(path):
    s = TopoDS_Shape()
    if not BRepTools.Read_s(s, path, BRep_Builder()):
        return None
    out = []
    ex = TopExp_Explorer(s, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current())
        g = GProp_GProps(); BRepGProp.SurfaceProperties_s(f, g)
        ad = BRepAdaptor_Surface(f)
        t = ad.GetType()
        u0, u1, v0, v1 = ad.FirstUParameter(), ad.LastUParameter(), ad.FirstVParameter(), ad.LastVParameter()
        cand = []
        if t == GeomAbs_Plane and all(map(math.isfinite, (u0, u1, v0, v1))):
            cand.append(min(abs(u1 - u0), abs(v1 - v0)) / math.sqrt(2))
        elif t == GeomAbs_Cone and math.isfinite(v0) and math.isfinite(v1):
            try:
                a = ad.Cone().SemiAngle(); sl = abs(v1 - v0)
                cand += [abs(sl * math.cos(a)), abs(sl * math.sin(a))]
            except Exception:
                pass
        out.append((g.Mass(), cand))
        ex.Next()
    return out


def sample(keyword):
    random.seed(42)
    c = []
    for py in glob.glob(os.path.join(ROOT, 'output', '*', 'cadquery.py')):
        src = open(py, encoding='utf-8', errors='replace').read()
        vals = [float(v) for nm, v in PARAM_RE.findall(src) if keyword in nm.lower() and float(v) > 0]
        if vals:
            c.append((os.path.dirname(py), vals))
    random.shuffle(c)
    return c[:300]


def stats(xs):
    xs = np.array(xs)
    return dict(median=round(float(np.median(xs)), 4), p5=round(float(np.quantile(xs, 0.05)), 4),
                min=round(float(xs.min()), 4))


res = {}
areas_all, smallest_all = [], []
for key in ('fillet', 'chamfer'):
    cands = sample(key)
    cov = {N: [] for N in NS}
    tot_areas, smallest = [], []
    matched = 0
    for d, vals in cands:
        fl = faces(os.path.join(d, 'model.brep'))
        if not fl:
            continue
        tot = sum(a for a, _ in fl)
        tot_areas.append(tot); smallest.append(min(a for a, _ in fl))
        if key == 'chamfer':
            ch = sum(a for a, cand in fl if any(near(x, vals) for x in cand))
            if ch > 0:
                matched += 1
                for N in NS:
                    cov[N].append(1 - (1 - ch / tot) ** N)
    areas_all += tot_areas; smallest_all += smallest
    entry = dict(n_models=len(cands), median_part_area_mm2=round(float(np.median(tot_areas)), 1),
                 smallest_face_area_mm2=dict(median=round(float(np.median(smallest)), 4),
                                             p5=round(float(np.quantile(smallest, 0.05)), 5)))
    if key == 'chamfer':
        entry.update(n_with_matched_chamfer_faces=matched,
                     chamfer_surface_coverage={N: stats(cov[N]) for N in NS})
    res[key] = entry

frac99 = 1 - 0.01 ** (1 / 8192)          # face share needed for P>=0.99 at N=8192
Amed = float(np.median(areas_all))
res['reliable_coverage_at_8192'] = dict(min_area_fraction=frac99, median_part_area_mm2=round(Amed, 1),
                                        min_face_area_mm2_at_median_part=round(frac99 * Amed, 2))
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(ROOT, '_review', 'exp_d2_chamfer_coverage.json'), 'w'), indent=1)
