# -*- coding: utf-8 -*-
"""实验S: 预测结果的建模精度 v2 —— 导师要求的位置 / 角度 / 特征边 / 特征点 / 约束(代理) / 可编辑性 (实测).
对 400 件测试子集, 每个方法:
  预测 B-rep 按真值最长边等比缩放并平移到真值包围盒中心 (与实验Q同一对齐), 然后
  * 位置: 孔轴 (圆柱面按轴线聚类为唯一轴) 的轴上参考点, 真值->预测就近匹配 (同向轴), 误差 mm 中位数 / <=0.5 mm 比例; 孔数召回;
  * 角度: 程序中具名 *angle* 参数 vs 预测几何角度候选 (圆锥全角、圆柱/圆环面角向范围、平行孔轴绕中心的角间距), <=1 deg 命中率;
  * 特征边: 两 B-rep 所有边等弧长采样点的双向 Chamfer 距离 (mm); 特征点: 真值顶点到最近预测顶点距离中位数 / <=0.5 mm 比例;
  * 约束代理: 隐含几何关系 —— 同轴 (同轴不同径: 孔+凸台), 等径不同轴 (孔阵列), 平行轴, 唯一平面法向数; 报告各关系真值计数被预测覆盖的比例;
  * 可编辑性: 取预测程序第一个尺寸类具名参数 x1.1 重新执行: 可执行率、几何随之变化率 (体积或包围盒变化 > 0.1%).
用法: conda run -n cadfit-env python exp_s_precision2.py  (父进程要 scipy; 子进程 = cadquery env) <pred_dir_name> [...]
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, sys, json, re, math, ast
import numpy as np
ROOT = _ROOT
PRED = os.path.join(ROOT, 'predictions'); OUT = os.path.join(ROOT, 'output')
sys.path.insert(0, os.path.join(ROOT, '_review'))
from guarded_exec import run_guarded_batch
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Torus, GeomAbs_Plane, GeomAbs_Cone
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRep import BRep_Tool
from OCP.GCPnts import GCPnts_AbscissaPoint
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)
test = [l.strip() for l in open(os.path.join(PRED, 'test_subset.txt'), encoding='utf-8') if l.strip()]
test = test[:int(os.environ.get('EXP_S_LIMIT', len(test)))]
_GT = {}


# ------------------------------------------------------------------ probe (runs inside the guarded cadquery subprocess)
def probe(shape):
    b = Bnd_Box(); BRepBndLib.Add_s(shape, b, True); x0, y0, z0, x1, y1, z1 = b.Get()
    cyl, cone, tor_ext, planes = [], [], [], []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current()); ad = BRepAdaptor_Surface(f); t = ad.GetType()
        u0, u1, v0, v1 = ad.FirstUParameter(), ad.LastUParameter(), ad.FirstVParameter(), ad.LastVParameter()
        if t == GeomAbs_Cylinder:
            c = ad.Cylinder(); ax = c.Axis(); d = ax.Direction(); p = ax.Location()
            ext = abs(u1 - u0) if all(map(math.isfinite, (u0, u1))) else 0.0
            cyl.append([c.Radius(), d.X(), d.Y(), d.Z(), p.X(), p.Y(), p.Z(), math.degrees(ext)])
        elif t == GeomAbs_Cone:
            cone.append(math.degrees(2 * abs(ad.Cone().SemiAngle())))
        elif t == GeomAbs_Torus:
            if all(map(math.isfinite, (u0, u1))): tor_ext.append(math.degrees(abs(u1 - u0)))
        elif t == GeomAbs_Plane:
            n = ad.Plane().Axis().Direction(); planes.append([n.X(), n.Y(), n.Z()])
        ex.Next()
    # edges: arc-length sampling, budget ~600 points
    edges = []; lens = []
    ex = TopExp_Explorer(shape, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge_s(ex.Current()); cu = BRepAdaptor_Curve(e)
        try:
            L = GCPnts_AbscissaPoint.Length_s(cu)
        except Exception:
            L = 0.0
        edges.append(cu); lens.append(L); ex.Next()
    tot = sum(lens) or 1.0; pts = []
    for cu, L in zip(edges, lens):
        n = max(2, int(round(600 * L / tot)))
        a, bb = cu.FirstParameter(), cu.LastParameter()
        for i in range(n):
            p = cu.Value(a + (bb - a) * (i + 0.5) / n); pts.append([p.X(), p.Y(), p.Z()])
    verts = []; seen = set()
    ex = TopExp_Explorer(shape, TopAbs_VERTEX)
    while ex.More():
        p = BRep_Tool.Pnt_s(TopoDS.Vertex_s(ex.Current())); k = (round(p.X(), 4), round(p.Y(), 4), round(p.Z(), 4))
        if k not in seen:
            seen.add(k); verts.append(list(k))
        ex.Next()
    gp = GProp_GProps(); BRepGProp.VolumeProperties_s(shape, gp)
    return dict(bbox=[x0, y0, z0, x1, y1, z1], cyl=cyl, cone=cone, tor_ext=tor_ext, planes=planes,
                edge_pts=pts[:1200], verts=verts[:400], volume=gp.Mass())


# ------------------------------------------------------------------ analysis helpers (parent process)
def align(rp, gb):
    """缩放 + 平移: 预测包围盒最长边 -> 真值最长边, 中心重合. 返回 (k, t): x' = k*x + t."""
    pb = np.array(rp['bbox']); gext = gb[3:] - gb[:3]; pext = pb[3:] - pb[:3]
    k = gext.max() / max(pext.max(), 1e-9)
    t = (gb[:3] + gb[3:]) / 2 - k * (pb[:3] + pb[3:]) / 2
    return k, t


def hole_axes(cyl, k=1.0, t=np.zeros(3)):
    """圆柱面 -> 唯一轴 (方向, 轴上最近原点的参考点, 半径). 同轴 = 方向平行且轴线距离 < 0.05 mm (缩放后)."""
    axes = []
    for r, dx, dy, dz, px, py, pz, ext in cyl:
        d = np.array([dx, dy, dz]); d = d / (np.linalg.norm(d) + 1e-12)
        p = k * np.array([px, py, pz]) + t
        p0 = p - d * np.dot(p, d)          # 轴上离原点最近的点 (轴线的规范表示)
        if d[np.argmax(np.abs(d))] < 0:
            d = -d
        R = k * r
        for a in axes:
            if abs(abs(np.dot(a['d'], d)) - 1) < 1e-3 and np.linalg.norm(a['p0'] - p0) < 0.05:
                a['radii'].add(round(R, 3)); break
        else:
            axes.append(dict(d=d, p0=p0, radii={round(R, 3)}))
    return axes


def relations(axes, planes):
    conc = sum(1 for a in axes if len(a['radii']) > 1)                       # 同轴不同径 (孔+沉孔/凸台)
    eq = 0; par = 0
    for i in range(len(axes)):
        for j in range(i + 1, len(axes)):
            if axes[i]['radii'] & axes[j]['radii']: eq += 1
            if abs(abs(np.dot(axes[i]['d'], axes[j]['d'])) - 1) < 1e-3: par += 1
    normals = []
    for n in planes:
        n = np.array(n); n = n / (np.linalg.norm(n) + 1e-12)
        if not any(abs(abs(np.dot(n, m)) - 1) < 1e-3 for m in normals):
            normals.append(n)
    perp = sum(1 for i in range(len(normals)) for j in range(i + 1, len(normals)) if abs(np.dot(normals[i], normals[j])) < 1e-3)
    return dict(concentric=conc, equal_radius=eq, parallel_axis=par, plane_dirs=len(normals), perpendicular_planes=perp)


def angle_candidates(rp, k, t):
    c = list(rp['cone']) + [x[7] for x in rp['cyl'] if 0 < x[7] < 359.9] + [x for x in rp['tor_ext'] if 0 < x < 359.9]
    axes = hole_axes(rp['cyl'], k, t)
    # 平行孔轴绕其质心的角间距
    for d0 in ({tuple(np.round(a['d'], 3)) for a in axes}):
        grp = [a for a in axes if abs(abs(np.dot(a['d'], np.array(d0))) - 1) < 1e-3]
        if len(grp) < 3: continue
        d = np.array(d0); ctr = np.mean([a['p0'] for a in grp], axis=0)
        e1 = np.cross(d, [1, 0, 0]); e1 = e1 if np.linalg.norm(e1) > 1e-3 else np.cross(d, [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
        ang = sorted(math.degrees(math.atan2(np.dot(a['p0'] - ctr, e2), np.dot(a['p0'] - ctr, e1))) % 360 for a in grp)
        c += [(ang[(i + 1) % len(ang)] - ang[i]) % 360 for i in range(len(ang))]
    return [x for x in c if x > 0.5]


def chamfer(A, B):
    A, B = np.asarray(A), np.asarray(B)
    if len(A) == 0 or len(B) == 0: return None
    from scipy.spatial import cKDTree
    return float(0.5 * (cKDTree(B).query(A)[0].mean() + cKDTree(A).query(B)[0].mean()))


def named_params(code):
    return [(nm, float(v)) for nm, v in PARAM_RE.findall(code)]


def edit_variant(code):
    """第一个尺寸类具名参数 x1.1; 返回 (新代码, 参数名) 或 None."""
    for nm, v in named_params(code):
        low = nm.lower()
        if v > 0 and any(kw in low for kw in ('dia', 'radius', 'width', 'length', 'height', 'thick', 'depth', 'size', 'chamfer', 'fillet')) \
                and not any(kw in low for kw in ('count', 'num', 'angle')):
            new = re.sub(r"^(%s\s*=\s*)(-?\d+\.?\d*)\s*$" % re.escape(nm), lambda m: m.group(1) + repr(round(v * 1.1, 4)), code, count=1, flags=re.M)
            if new != code: return new, nm
    return None


def evaluate(pred_name):
    global _GT
    pdir = os.path.join(PRED, pred_name)
    if not _GT:
        _GT = run_guarded_batch([(u, open(os.path.join(OUT, u, 'cadquery.py'), encoding='utf-8', errors='replace').read()) for u in test],
                                'exp_s_precision2', 'probe', mem_gb=3.0, per_item_timeout=90)
        print('  GT probed ok %d' % sum(1 for v in _GT.values() if v[0]), flush=True)
    items = [(u, open(os.path.join(pdir, u + '.py'), encoding='utf-8', errors='replace').read()) for u in test if os.path.isfile(os.path.join(pdir, u + '.py'))]
    pres = run_guarded_batch(items, 'exp_s_precision2', 'probe', mem_gb=3.0, per_item_timeout=90)
    print('  predictions probed ok %d / %d' % (sum(1 for v in pres.values() if v[0]), len(items)), flush=True)
    # editability variants (only for executing predictions with a dimensional named parameter)
    ed_items, ed_name = [], {}
    for u, code in items:
        if pres.get(u, (False,))[0]:
            ev = edit_variant(code)
            if ev: ed_items.append((u, ev[0])); ed_name[u] = ev[1]
    eres = run_guarded_batch(ed_items, 'exp_s_precision2', 'probe', mem_gb=3.0, per_item_timeout=90) if ed_items else {}
    pos_err, pos_n_gt, pos_n_matched, hole_recall = [], 0, 0, []
    ang_hit, ang_n, ang_err = 0, 0, []
    edge_cd, vert_err, vert_hit, vert_n = [], [], 0, 0
    rel_cov = {k: [0, 0] for k in ('concentric', 'equal_radius', 'parallel_axis', 'perpendicular_planes')}
    ed_exec = ed_change = 0; n_pairs = 0
    for u, code in items:
        okg, rg = _GT.get(u, (False, None)); okp, rp = pres.get(u, (False, None))
        if not (okg and okp): continue
        gb = np.array(rg['bbox'])
        if (gb[3:] - gb[:3]).max() < 1e-6 or (np.array(rp['bbox'])[3:] - np.array(rp['bbox'])[:3]).max() < 1e-6: continue
        n_pairs += 1
        k, t = align(rp, gb)
        # 位置
        ga, pa = hole_axes(rg['cyl']), hole_axes(rp['cyl'], k, t)
        pos_n_gt += len(ga); used = set(); m = 0
        for a in ga:
            best = None
            for j, b in enumerate(pa):
                if j in used or abs(abs(np.dot(a['d'], b['d'])) - 1) > 1e-2: continue
                dd = np.linalg.norm(a['p0'] - b['p0'])
                if best is None or dd < best[0]: best = (dd, j)
            if best is not None and best[0] < 5.0:
                used.add(best[1]); pos_err.append(float(best[0])); m += 1
        pos_n_matched += m; hole_recall.append(m / len(ga) if ga else np.nan)
        # 角度
        gsrc = open(os.path.join(OUT, u, 'cadquery.py'), encoding='utf-8', errors='replace').read()
        cands = angle_candidates(rp, k, t)
        for nm, v in named_params(gsrc):
            if 'angle' in nm.lower() and 0 < v < 360:
                ang_n += 1
                if cands:
                    e = min(min(abs(c - v), abs(c - (360 - v))) for c in cands); ang_err.append(e)
                    if e <= 1.0: ang_hit += 1
        # 特征边 / 点
        P = k * np.array(rp['edge_pts']) + t if rp['edge_pts'] else np.zeros((0, 3))
        cd = chamfer(rg['edge_pts'], P)
        if cd is not None: edge_cd.append(cd)
        if rg['verts'] and rp['verts']:
            from scipy.spatial import cKDTree
            V = k * np.array(rp['verts']) + t
            d = cKDTree(V).query(np.array(rg['verts']))[0]
            vert_err += d.tolist(); vert_hit += int((d <= 0.5).sum()); vert_n += len(d)
        # 约束代理
        rgl, rpl = relations(ga, rg['planes']), relations(pa, rp['planes'])
        for kk in rel_cov:
            rel_cov[kk][0] += min(rgl[kk], rpl[kk]); rel_cov[kk][1] += rgl[kk]
        # 可编辑性
        if u in eres:
            oke, re_ = eres[u]
            if oke:
                ed_exec += 1
                v0, v1 = rp['volume'], re_['volume']; b0, b1 = np.array(rp['bbox']), np.array(re_['bbox'])
                if abs(v1 - v0) > 1e-3 * abs(v0) or np.abs(b1 - b0).max() > 1e-3 * (b0[3:] - b0[:3]).max():
                    ed_change += 1
    pe = np.array(pos_err) if pos_err else np.array([np.nan]); ve = np.array(vert_err) if vert_err else np.array([np.nan])
    out = dict(method=pred_name, n_pairs=n_pairs,
               holes_gt=pos_n_gt, holes_matched=pos_n_matched, hole_match_rate=round(pos_n_matched / max(1, pos_n_gt), 4),
               hole_pos_err_median_mm=round(float(np.nanmedian(pe)), 3), hole_pos_within_0p5mm=round(float(np.mean(pe <= 0.5)), 4) if pos_err else None,
               angle_params=ang_n, angle_hit_1deg=round(ang_hit / max(1, ang_n), 4), angle_err_median_deg=round(float(np.median(ang_err)), 2) if ang_err else None,
               edge_chamfer_median_mm=round(float(np.median(edge_cd)), 3) if edge_cd else None,
               vertex_err_median_mm=round(float(np.nanmedian(ve)), 3), vertex_within_0p5mm=round(vert_hit / max(1, vert_n), 4), vertices_gt=vert_n,
               relation_coverage={k: dict(gt=v[1], covered=v[0], rate=round(v[0] / max(1, v[1]), 4)) for k, v in rel_cov.items()},
               edit_tested=len(ed_items), edit_executes=round(ed_exec / max(1, len(ed_items)), 4) if ed_items else None,
               edit_geometry_changes=round(ed_change / max(1, len(ed_items)), 4) if ed_items else None)
    return out


if __name__ == '__main__':
    pj = os.path.join(ROOT, '_review', 'exp_s_precision2.json')
    prev = json.load(open(pj)) if os.path.exists(pj) else {}
    for name in sys.argv[1:]:
        o = evaluate(name); prev[name] = o
        print(json.dumps(o, indent=1), flush=True)
        json.dump(prev, open(pj, 'w'), indent=1)
