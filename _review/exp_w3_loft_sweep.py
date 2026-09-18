# -*- coding: utf-8 -*-
u"""实验W3: loft 截面数 / sweep 路径长度 测量器 (批注 p45 "per-operation measurers" 最后两项).

论文此前称 loft 的截面数与 sweep 的路径在 B-rep 里"没有可读痕迹", 本实验把这句话验证到底:
要么给出能用的测量器, 要么给出"不可测"的具体证据 (B-rep 里有什么/没有什么, 在多少模型上失败, 为什么).

对每个含 .loft( 的模型 (379 个) 与含 .sweep( 的模型 (400 个):

  声明侧 (两条路):
    (a) 静态: 用 ast 解析 cadquery.py (沿用 exp_w2_revolve_axis 的 Program/walk_chain/ev),
        把喂给 .sweep( 的 path 链回溯到 cq.Workplane(...) 并在真实 Workplane 上重放
        (平面调用 + 纯草图调用), 再用 BRepGProp 线性属性量出路径长度;
        链里出现选择器/循环/函数/未知调用 -> "not statically resolvable" (与 exp_w2 同口径).
        另特判 cq.Wire.makeHelix(...) 这类非链式路径.
    (b) 动态: 在受保护的子进程里执行 cadquery.py, 钩住 Workplane.loft / Workplane._sweep,
        在调用现场取到 真正 的截面线集合 (ctx.pendingWires) 与 真正 的 path wire,
        并另建一份 未经后续布尔 的"原始特征体"(raw loft solid / raw swept solid).
        动态值是声明侧的 ground truth, 同时用来校验 (a) 的静态求解器.

  实测侧 (从 B-rep 反推, 两个层次):
    L1 "特征体": 在 raw loft / raw sweep 上量 —— 回答"这个特征自己的 B-rep 里带不带这个信息";
    L2 "交付件": 在 output/<uuid>/model.brep (STEP 往返后的发布件) 上量 —— 回答"经过后续布尔
        与 STEP 往返之后痕迹还在不在"; L2 的候选面由 与 L1 侧面 的几何重合 (BRepExtrema 点-面距离)
        匹配得到, 因此"没匹配上"= 该面已被布尔吃掉/裁掉.

  LOFT 截面数 N 的判据:
    ruled=True 时 N 段之间是 N-1 条独立面带, 数面带即可; 但本语料 379 个 loft 全是 ruled=False
    (默认光顺 loft), 面带判据无从适用 —— 光顺 loft 的中间截面平面上 没有棱边.
    光顺 loft 唯一残留的结构痕迹是逼近曲面在"沿 loft 方向"的 B 样条控制结构:
      OCCT BRepOffsetAPI_ThruSections(ruled=False) 用 GeomFill_AppSurf 以 C2/3 次逼近所有截面,
      若逼近对每个截面保留一个控制点, 则 沿 loft 方向的极点数 NbPoles == N (等价: 相异节点数 = N-2+1).
    因此 measured_N := 侧面 B 样条曲面 沿 loft 方向的极点数 (loft 方向 = 常参数等参线 沿轴向 展布为 0 的那个方向).
    另做"退化检验"回答 信息在不在 (与判据无关):
      (i) 逐个去掉中间截面重做 loft, 体积+面积 相对变化 < 1e-6 即该截面"不可见";
      (ii) 取 k 个等间隔截面重做 loft, 找出与全截面 loft 同形的最小 k (min_even_subset_reproducing).
           k < N 意味着 同一个 B-rep 也能由 k 个截面造出来 -> 声明的 N 在原理上不可恢复,
           此时判据给出的 measured_N 若 == k, 说明测量器量到的是 "有效截面数" 而不是错.

  SWEEP 路径长度 L 的判据 (Pappus/Guldinus):
    管状扫掠的 侧面积 = 截面周长 x 中心线长度, 体积 = 截面面积 x 中心线长度. 故
      L_area = (A_total - 2*A_cap) / perimeter,  L_vol = V / A_profile
    两个互相独立的估计量; 再辅以 沿扫掠方向 等参线长度的 min/mean/max 作区间校验.
    L2 上用 匹配到的侧面积 / 周长 复算, 面被裁掉多少就差多少 -> 直接给出失配归因.

报告口径与 exp_g_measurers / exp_w2_revolve_axis 一致: attempted / exactly matched / close /
no candidate / not statically resolvable + 误差分布 + 失配归因 + 例子 UUID.

用法:
  python exp_w3_loft_sweep.py [--sample N] [--seed 42] [--limit N] [--chunk 6]
                              [--state <partial.jsonl>] [--worker <listfile>]
输出: _review/exp_w3_loft_sweep.json + exp_w3_loft_sweep_records.jsonl (+ exp_w3_run.log)
"""
import sys, os, re, json, math, time, ast, random, collections, subprocess, tempfile, threading

ROOT = r'E:/3005/data'
OUT = os.path.join(ROOT, 'output')
REV_DIR = os.path.join(ROOT, '_review')
sys.path.insert(0, REV_DIR)

# ---- 容差 -------------------------------------------------------------------
REL_EXACT = 1e-6          # "exactly matched": 相对误差 <= 1e-6
REL_CLOSE = 1e-3          # "close": 相对误差 <= 1e-3 (0.1%)
ABS_CLOSE = 0.01          # 或 绝对误差 <= 0.01 mm
GEO_TOL = 1e-4            # 面匹配的点-面距离 (mm)
DEGEN_REL = 1e-6          # 退化检验: 体积/面积 相对变化阈值

import cadquery as cq
from cadquery.occ_impl.shapes import loft as occ_loft
from OCP.BRep import BRep_Builder, BRep_Tool
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_IN, TopAbs_ON
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCP.GeomAbs import (GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere,
                         GeomAbs_Torus, GeomAbs_BezierSurface, GeomAbs_BSplineSurface,
                         GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion,
                         GeomAbs_OffsetSurface, GeomAbs_OtherSurface)
from OCP.Geom import Geom_BSplineSurface, Geom_BezierSurface, Geom_RectangularTrimmedSurface
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.GeomAdaptor import GeomAdaptor_Curve
from OCP.GCPnts import GCPnts_AbscissaPoint
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepTopAdaptor import BRepTopAdaptor_FClass2d
from OCP.gp import gp_Pnt, gp_Pnt2d

SURF_NAME = {GeomAbs_Plane: 'plane', GeomAbs_Cylinder: 'cylinder', GeomAbs_Cone: 'cone',
             GeomAbs_Sphere: 'sphere', GeomAbs_Torus: 'torus', GeomAbs_BezierSurface: 'bezier',
             GeomAbs_BSplineSurface: 'bspline', GeomAbs_SurfaceOfRevolution: 'revolution',
             GeomAbs_SurfaceOfExtrusion: 'extrusion', GeomAbs_OffsetSurface: 'offset',
             GeomAbs_OtherSurface: 'other'}


# ============================================================ 小工具
def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _norm(a):
    return math.sqrt(_dot(a, a))


def _unit(a):
    n = _norm(a)
    return (a[0] / n, a[1] / n, a[2] / n) if n > 1e-12 else (0.0, 0.0, 1.0)


def TS(x):
    """cadquery Shape / TopoDS_Shape -> TopoDS_Shape."""
    return x.wrapped if hasattr(x, 'wrapped') else x


def faces_of(shape):
    shape = TS(shape)
    out = []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        out.append(TopoDS.Face_s(ex.Current()))
        ex.Next()
    return out


def area_of(shape):
    p = GProp_GProps()
    BRepGProp.SurfaceProperties_s(TS(shape), p)
    return p.Mass()


def volume_of(shape):
    p = GProp_GProps()
    BRepGProp.VolumeProperties_s(TS(shape), p)
    return p.Mass()


def length_of(shape):
    p = GProp_GProps()
    BRepGProp.LinearProperties_s(TS(shape), p)
    return p.Mass()


def centroid_linear(shape):
    p = GProp_GProps()
    BRepGProp.LinearProperties_s(TS(shape), p)
    c = p.CentreOfMass()
    return (c.X(), c.Y(), c.Z())


def centroid_surface(shape):
    p = GProp_GProps()
    BRepGProp.SurfaceProperties_s(TS(shape), p)
    c = p.CentreOfMass()
    return (c.X(), c.Y(), c.Z())


def shape_dist(a, b):
    try:
        d = BRepExtrema_DistShapeShape(TS(a), TS(b))
        d.Perform()
        return d.Value() if d.IsDone() else None
    except Exception:
        return None


def bbox_of(shape, pad=0.0):
    b = Bnd_Box()
    BRepBndLib.Add_s(TS(shape), b)
    if b.IsVoid():
        return None
    xm, ym, zm, xM, yM, zM = b.CornerMin().X(), b.CornerMin().Y(), b.CornerMin().Z(), \
        b.CornerMax().X(), b.CornerMax().Y(), b.CornerMax().Z()
    return (xm - pad, ym - pad, zm - pad, xM + pad, yM + pad, zM + pad)


def bbox_overlap(a, b):
    if a is None or b is None:
        return False
    return not (a[3] < b[0] or b[3] < a[0] or a[4] < b[1] or b[4] < a[1] or a[5] < b[2] or b[5] < a[2])


def sample_wire(w, n_per_edge=8):
    """在 wire/edge 上采样 3D 点."""
    w = TS(w)
    pts = []
    ex = TopExp_Explorer(w, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge_s(ex.Current())
        try:
            ad = BRepAdaptor_Curve(e)
            t0, t1 = ad.FirstParameter(), ad.LastParameter()
            for i in range(n_per_edge):
                t = t0 + (t1 - t0) * i / max(1, n_per_edge - 1)
                p = ad.Value(t)
                pts.append((p.X(), p.Y(), p.Z()))
        except Exception:
            pass
        ex.Next()
    return pts


def plane_fit(pts):
    """最小二乘平面: 返回 (normal, rms_residual, size). 点太少返回 None."""
    if len(pts) < 3:
        return None
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    cz = sum(p[2] for p in pts) / n
    # 3x3 协方差
    m = [[0.0] * 3 for _ in range(3)]
    for p in pts:
        d = (p[0] - cx, p[1] - cy, p[2] - cz)
        for i in range(3):
            for j in range(3):
                m[i][j] += d[i] * d[j]
    try:
        import numpy as np
        w, v = np.linalg.eigh(np.array(m))
        nrm = tuple(float(x) for x in v[:, 0])
        resid = math.sqrt(max(0.0, float(w[0])) / n)
        size = math.sqrt(max(1e-30, float(w[2])) / n)
    except Exception:
        return None
    return nrm, resid, size


def surface_of(face):
    s = BRep_Tool.Surface_s(face)
    while isinstance(s, Geom_RectangularTrimmedSurface):
        s = s.BasisSurface()
    return s


def face_uv(face):
    ad = BRepAdaptor_Surface(face)
    return ad.FirstUParameter(), ad.LastUParameter(), ad.FirstVParameter(), ad.LastVParameter()


def iso_length(surf, is_u, t, a0, a1):
    """曲面 surf 在 u=t (is_u) 或 v=t 的等参线在 [a0,a1] 上的弧长."""
    try:
        c = surf.UIso(t) if is_u else surf.VIso(t)
        ga = GeomAdaptor_Curve(c, a0, a1)
        return GCPnts_AbscissaPoint.Length_s(ga)
    except Exception:
        return None


def iso_axial_spread(surf, is_u, t, a0, a1, axis, n=12):
    """常参数等参线上各点沿 axis 的投影跨度 (截面方向 -> ~0)."""
    try:
        c = surf.UIso(t) if is_u else surf.VIso(t)
    except Exception:
        return None
    vals = []
    for i in range(n):
        s = a0 + (a1 - a0) * i / (n - 1.0)
        try:
            p = c.Value(s)
        except Exception:
            return None
        vals.append(p.X() * axis[0] + p.Y() * axis[1] + p.Z() * axis[2])
    return max(vals) - min(vals)


def bspline_struct(surf):
    """B 样条/贝塞尔曲面的 UV 结构."""
    if isinstance(surf, Geom_BSplineSurface):
        return dict(kind='bspline', npu=surf.NbUPoles(), npv=surf.NbVPoles(),
                    nku=surf.NbUKnots(), nkv=surf.NbVKnots(),
                    du=surf.UDegree(), dv=surf.VDegree(),
                    uper=bool(surf.IsUPeriodic()), vper=bool(surf.IsVPeriodic()))
    if isinstance(surf, Geom_BezierSurface):
        return dict(kind='bezier', npu=surf.NbUPoles(), npv=surf.NbVPoles(),
                    nku=2, nkv=2, du=surf.UDegree(), dv=surf.VDegree(),
                    uper=False, vper=False)
    return None


def face_points_inside(face, k=5, want=9):
    """在 face 的有效裁剪域内取样 3D 点 (FClass2d 分类)."""
    u0, u1, v0, v1 = face_uv(face)
    if not all(map(math.isfinite, (u0, u1, v0, v1))):
        return []
    surf = BRep_Tool.Surface_s(face)
    try:
        cls = BRepTopAdaptor_FClass2d(face, 1e-6)
    except Exception:
        cls = None
    pts = []
    for i in range(k):
        for j in range(k):
            u = u0 + (u1 - u0) * (i + 0.5) / k
            v = v0 + (v1 - v0) * (j + 0.5) / k
            if cls is not None:
                try:
                    st = cls.Perform(gp_Pnt2d(u, v))
                    if st not in (TopAbs_IN, TopAbs_ON):
                        continue
                except Exception:
                    pass
            try:
                p = surf.Value(u, v)
            except Exception:
                continue
            pts.append((p.X(), p.Y(), p.Z()))
            if len(pts) >= want:
                return pts
    if not pts:
        try:
            p = surf.Value((u0 + u1) / 2, (v0 + v1) / 2)
            pts.append((p.X(), p.Y(), p.Z()))
        except Exception:
            pass
    return pts


def point_face_dist(pt, face):
    try:
        v = BRepBuilderAPI_MakeVertex(gp_Pnt(*pt)).Vertex()
        d = BRepExtrema_DistShapeShape(v, face)
        d.Perform()
        return d.Value() if d.IsDone() else None
    except Exception:
        return None


def survival_fraction(raw_faces, released_faces, npts=9, tol=GEO_TOL):
    """在 raw 特征面上取样, 统计仍落在 发布件边界 上的点比例.
    对 布尔把面切碎 或 与相邻面合并 都稳健 (只看点在不在边界上), 因此比 面匹配 更可靠."""
    tot = hit = 0
    for f in raw_faces:
        pts = face_points_inside(f, k=5, want=npts)
        for pt in pts:
            tot += 1
            for rf, rb in released_faces:
                if rb is None or not (rb[0] <= pt[0] <= rb[3] and rb[1] <= pt[1] <= rb[4]
                                      and rb[2] <= pt[2] <= rb[5]):
                    continue
                d = point_face_dist(pt, rf)
                if d is not None and d <= tol:
                    hit += 1
                    break
    return (hit / tot if tot else None), tot


def face_lies_on(face_b, face_a, tol=GEO_TOL, nmax=5):
    """face_b 的采样点是否都落在 face_a (裁剪后) 上 -> b 是 a 的残片."""
    pts = face_points_inside(face_b)[:nmax]
    if not pts:
        return False, None
    ds = []
    for p in pts:
        d = point_face_dist(p, face_a)
        if d is None:
            return False, None
        ds.append(d)
    return (max(ds) <= tol), round(max(ds), 8)


# ============================================================ 声明侧: 静态求解 (sweep path)
import exp_w2_revolve_axis as W2       # 复用 exp_w2 的 ast 求值器/链回溯 (同口径)

Unresolvable = W2.Unresolvable
PATH_OPS = set(W2.SKETCH_OK) | set(W2.PLANE_OPS) | {'wire', 'close', 'consolidateWires', 'add'}


def replay_path_chain(prog, root, ops, before_line):
    """在真实 cq.Workplane 上重放 path 链 (平面调用 + 纯草图调用)."""
    ra = W2.call_args(prog, root, before_line, ['inPlane', 'origin', 'obj'])
    if 'obj' in ra:
        raise Unresolvable('workplane_obj_kw')
    in_plane = ra.get('inPlane', 'XY')
    origin = ra.get('origin', (0, 0, 0))
    if isinstance(in_plane, str):
        wp = cq.Workplane(in_plane, origin=tuple(float(x) for x in origin))
    elif isinstance(in_plane, cq.Plane):
        wp = cq.Workplane(in_plane)
    else:
        raise Unresolvable('workplane_arg_type')
    for m, call in ops:
        if m not in PATH_OPS:
            raise Unresolvable('chain_op:' + m)
        args = [prog.ev(a, before_line) for a in call.args]
        kwargs = {}
        for k in call.keywords:
            if k.arg is None:
                raise Unresolvable('star_kwargs')
            kwargs[k.arg] = prog.ev(k.value, before_line)
        args = [list(a) if isinstance(a, tuple) and a and isinstance(a[0], tuple) else a for a in args]
        for k, v in list(kwargs.items()):
            if isinstance(v, tuple) and v and isinstance(v[0], tuple):
                kwargs[k] = list(v)
        try:
            wp = getattr(wp, m)(*args, **kwargs)
        except Exception as e:
            raise Unresolvable('replay:' + m + ':' + type(e).__name__)
        if not isinstance(wp, cq.Workplane):
            raise Unresolvable('replay_not_workplane:' + m)
    return wp


def static_helix(prog, node, before_line):
    """特判 cq.Wire.makeHelix(pitch, height, radius, center, dir, angle, lefthand)."""
    f = node.func
    if not (isinstance(f, ast.Attribute) and f.attr in ('makeHelix', 'makeCircle', 'makePolygon')
            and isinstance(f.value, ast.Attribute) and f.value.attr in ('Wire', 'Edge')
            and isinstance(f.value.value, ast.Name) and f.value.value.id in ('cq', 'cadquery')):
        raise Unresolvable('not_static_ctor')
    args = [prog.ev(a, before_line) for a in node.args]
    kwargs = {k.arg: prog.ev(k.value, before_line) for k in node.keywords if k.arg}
    cls = getattr(cq, f.value.attr)
    fn = getattr(cls, f.attr)
    try:
        if f.attr == 'makeHelix':
            names = ['pitch', 'height', 'radius', 'center', 'dir', 'angle', 'lefthand']
            kw = dict(zip(names, args))
            kw.update(kwargs)
            for key in ('center', 'dir'):
                if key in kw and not isinstance(kw[key], cq.Vector):
                    kw[key] = cq.Vector(*kw[key])
            w = fn(**kw)
        else:
            w = fn(*args, **kwargs)
    except Exception as e:
        raise Unresolvable('ctor:' + type(e).__name__)
    return w


def path_expr_length(prog, expr, before_line, src):
    """把 path 表达式解析成 wire 并量长度. 抛 Unresolvable."""
    node = expr
    # 变量 -> 模块级唯一赋值
    seen = 0
    while isinstance(node, ast.Name):
        seen += 1
        if seen > 8:
            raise Unresolvable('name_chain_depth')
        ln = prog.top_assign.get(node.id, (None, None))[0]
        node = prog.name_value(node.id, before_line)
        before_line = ln if ln else before_line
    if isinstance(node, ast.Call) and not W2.is_workplane_ctor(node):
        f = node.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Attribute):
            w = static_helix(prog, node, before_line)
            return length_of(w.wrapped), 'static_ctor:' + f.attr
    root, ops = W2.walk_chain(prog, node, before_line)
    wp = replay_path_chain(prog, root, ops, before_line)
    obj = None
    try:
        obj = wp.wire().val()
    except Exception:
        obj = None
    if obj is None or not hasattr(obj, 'wrapped'):
        obj = wp.val()
    if obj is None or not hasattr(obj, 'wrapped') or obj.wrapped is None:
        raise Unresolvable('no_wire')
    L = length_of(obj.wrapped)
    if not (L > 0):
        raise Unresolvable('zero_length')
    return L, 'chain'


def static_sweep_paths(src):
    """对源码里每个 .sweep( 调用静态求 path 长度. 返回按源码顺序的列表."""
    try:
        prog = W2.Program(src)
    except SyntaxError:
        return [dict(ok=False, reason='syntax_error', line=0)]
    calls = [n for n in ast.walk(prog.tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'sweep']
    calls.sort(key=lambda n: (n.lineno, n.col_offset))
    out = []
    for c in calls:
        rec = dict(line=c.lineno)
        try:
            if not prog.is_top_level(c):
                raise Unresolvable('sweep_nested')
            stmt = prog.stmt_of(c)
            before = stmt.lineno
            pexpr = None
            if c.args:
                pexpr = c.args[0]
            else:
                for k in c.keywords:
                    if k.arg == 'path':
                        pexpr = k.value
            if pexpr is None:
                raise Unresolvable('no_path_arg')
            L, how = path_expr_length(prog, pexpr, before, src)
            rec.update(ok=True, path_len=round(L, 9), how=how)
        except Unresolvable as e:
            rec.update(ok=False, reason=str(e))
        except RecursionError:
            rec.update(ok=False, reason='recursion')
        except Exception as e:
            rec.update(ok=False, reason='exc:' + type(e).__name__ + ':' + str(e)[:50])
        out.append(rec)
    return out


# ============================================================ 动态侧: 执行 + 钩子
CAPTURED = {'loft': [], 'sweep': []}
_orig_loft = cq.Workplane.loft
_orig_sweep = cq.Workplane._sweep


def _hook_loft(self, ruled=False, combine=True, clean=True):
    from cadquery.occ_impl.shapes import Vertex
    try:
        if self.ctx.pendingWires:
            toLoft = list(self.ctx.pendingWires)
        else:
            toLoft = [el if isinstance(el, Vertex) else el.outerWire() for el in self._getFacesVertices()]
    except Exception:
        toLoft = []
    res = _orig_loft(self, ruled=ruled, combine=combine, clean=clean)
    raw = None
    try:
        if len(toLoft) >= 2:
            raw = occ_loft(toLoft, cap=True, ruled=ruled)
    except Exception:
        raw = None
    CAPTURED['loft'].append(dict(sections=toLoft, ruled=bool(ruled), raw=raw, combine=combine))
    return res


def _hook_sweep(self, path, multisection=False, makeSolid=True, isFrenet=False,
                transition='right', normal=None, auxSpine=None):
    from cadquery.occ_impl.shapes import Face, Compound, wiresToFaces
    try:
        p = path.val() if isinstance(path, cq.Workplane) else path
    except Exception:
        p = None
    # 注意: _getFaces() 会 pop 掉 pendingWires, 不能在原函数之前调用; 这里只做只读快照
    pending = list(self.ctx.pendingWires) if self.ctx.pendingWires else []
    objs = list(self.objects)
    res = _orig_sweep(self, path, multisection, makeSolid, isFrenet, transition, normal, auxSpine)
    profiles = []
    try:
        for el in objs:
            if isinstance(el, Face):
                profiles.append(el)
            elif isinstance(el, Compound):
                profiles.extend(s for s in el if isinstance(s, Face))
        if not profiles and pending:
            profiles = list(wiresToFaces(pending))
    except Exception:
        profiles = []
    CAPTURED['sweep'].append(dict(path=p, profiles=profiles, raw=res, multisection=bool(multisection),
                                  makeSolid=bool(makeSolid), isFrenet=bool(isFrenet), transition=transition))
    return res


def install_hooks():
    cq.Workplane.loft = _hook_loft
    cq.Workplane._sweep = _hook_sweep


def exec_program(path_py):
    CAPTURED['loft'] = []
    CAPTURED['sweep'] = []
    src = open(path_py, encoding='utf-8', errors='replace').read()
    g = {'__name__': '__cqx__', '__file__': path_py}
    t0 = time.time()
    exec(compile(src, path_py, 'exec'), g)
    return src, g, time.time() - t0


def final_shape(g):
    res = g.get('result')
    if res is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                res = v
    if res is None:
        return None
    try:
        s = res.val() if hasattr(res, 'val') else res
        return s.wrapped if hasattr(s, 'wrapped') else s
    except Exception:
        return None


# ============================================================ LOFT 测量
def section_info(wires):
    """截面线的几何信息 + loft 轴 (截面平面法向)."""
    infos, normals = [], []
    for w in wires:
        sh = w.wrapped if hasattr(w, 'wrapped') else w
        try:
            pts = sample_wire(sh, 8)
            L = length_of(sh)
            c = centroid_linear(sh) if L > 0 else (pts[0] if pts else (0, 0, 0))
        except Exception:
            pts, L, c = [], 0.0, (0, 0, 0)
        fit = plane_fit(pts) if len(pts) >= 3 else None
        nrm = fit[0] if fit else None
        planar = bool(fit and fit[1] <= 1e-6 * max(1.0, fit[2]))
        infos.append(dict(len=round(L, 6), centroid=[round(x, 6) for x in c],
                          n_pts=len(pts), planar=planar))
        if nrm:
            normals.append(nrm)
    axis = None
    if normals:
        ref = normals[0]
        acc = [0.0, 0.0, 0.0]
        for n in normals:
            s = 1.0 if _dot(n, ref) >= 0 else -1.0
            for i in range(3):
                acc[i] += s * n[i]
        axis = _unit(tuple(acc))
    if axis is None or _norm(axis) < 0.5:
        c0 = infos[0]['centroid'] if infos else (0, 0, 0)
        c1 = infos[-1]['centroid'] if infos else (0, 0, 1)
        axis = _unit(_sub(c1, c0))
    parallel = all(abs(_dot(_unit(n), axis)) > 0.999 for n in normals) if normals else False
    return infos, axis, parallel


def loft_lateral_faces(shape, axis):
    """分出 盖面 (法向平行 axis 的平面) 与 侧面."""
    caps, lat = [], []
    for f in faces_of(shape):
        ad = BRepAdaptor_Surface(f)
        if ad.GetType() == GeomAbs_Plane:
            d = ad.Plane().Axis().Direction()
            if abs(_dot((d.X(), d.Y(), d.Z()), axis)) > 0.999:
                caps.append(f)
                continue
        lat.append(f)
    return caps, lat


def measure_loft_face(face, axis):
    """在一张侧面上数 沿 loft 方向 的极点数. 返回 dict 或 None."""
    surf = surface_of(face)
    st = bspline_struct(surf)
    ad = BRepAdaptor_Surface(face)
    tname = SURF_NAME.get(ad.GetType(), '?')
    out = dict(surf=tname, area=round(area_of(face), 4))
    if st is None:
        out.update(measurable=False, why='surface_not_bspline')
        return out
    out.update(st)
    u0, u1, v0, v1 = surf.Bounds()
    if not all(map(math.isfinite, (u0, u1, v0, v1))):
        out.update(measurable=False, why='unbounded')
        return out
    # 哪个方向的 常参数等参线 是"截面"(沿轴向跨度 ~0)
    spread_u, spread_v = [], []
    for fr in (0.25, 0.5, 0.75):
        su = iso_axial_spread(surf, True, u0 + (u1 - u0) * fr, v0, v1, axis)
        sv = iso_axial_spread(surf, False, v0 + (v1 - v0) * fr, u0, u1, axis)
        if su is not None:
            spread_u.append(su)
        if sv is not None:
            spread_v.append(sv)
    if not spread_u or not spread_v:
        out.update(measurable=False, why='iso_failed')
        return out
    mu, mv = sum(spread_u) / len(spread_u), sum(spread_v) / len(spread_v)
    out.update(axial_spread_uiso=round(mu, 6), axial_spread_viso=round(mv, 6))
    # u=const 等参线沿轴跨度大 -> u 是 loft 方向; v=const 跨度小 -> v 是截面方向
    if mv < mu:
        loft_dir, npoles, deg, nk, per = 'V', st['npv'], st['dv'], st['nkv'], st['vper']
    else:
        loft_dir, npoles, deg, nk, per = 'U', st['npu'], st['du'], st['nku'], st['uper']
    out.update(measurable=True, loft_dir=loft_dir, n_poles_along_loft=npoles,
               degree_along_loft=deg, n_knots_along_loft=nk, periodic_along_loft=bool(per),
               measured_n=npoles)
    return out


def loft_degeneracy(sections, raw, cap_interior=8):
    """退化检验: 去掉中间截面 / 只留首尾, 形状是否不变."""
    out = dict(tested=False)
    try:
        if raw is None or len(sections) < 3:
            return out
        V0, A0 = volume_of(raw), area_of(raw)
        if not (V0 > 0):
            return out
        out.update(tested=True, volume=round(V0, 6), area=round(A0, 6))
        n = len(sections)
        # 只留首尾
        try:
            r2 = occ_loft([sections[0], sections[-1]], cap=True, ruled=False)
            V2, A2 = volume_of(r2), area_of(r2)
            out.update(two_section_rel_dv=round(abs(V2 - V0) / V0, 9),
                       two_section_rel_da=round(abs(A2 - A0) / max(A0, 1e-9), 9))
            out['degenerate_to_2'] = (out['two_section_rel_dv'] <= DEGEN_REL and
                                      out['two_section_rel_da'] <= DEGEN_REL)
        except Exception as e:
            out['two_section_err'] = type(e).__name__
        # 逐个去掉中间截面
        idx = list(range(1, n - 1))
        truncated = len(idx) > cap_interior
        idx = idx[:cap_interior]
        invisible = 0
        devs = []
        for i in idx:
            sub = [s for j, s in enumerate(sections) if j != i]
            try:
                ri = occ_loft(sub, cap=True, ruled=False)
                Vi, Ai = volume_of(ri), area_of(ri)
                dv = abs(Vi - V0) / V0
                da = abs(Ai - A0) / max(A0, 1e-9)
                devs.append(round(max(dv, da), 9))
                if dv <= DEGEN_REL and da <= DEGEN_REL:
                    invisible += 1
            except Exception:
                devs.append(None)
        out.update(drop_one_tested=len(idx), drop_one_truncated=truncated,
                   drop_one_invisible=invisible, drop_one_devs=devs[:12])
        # 最小可复现截面数: 取 k 个"等间隔"截面重做 loft, 与全截面 loft 同形的最小 k.
        # k < N 说明 同一个 B-rep 也能由 k 个截面造出来 -> 声明的 N 在原理上不可恢复.
        mink, tested_k = n, []
        for k in range(2, min(n, 14)):
            sel = sorted(set(int(round(j * (n - 1) / (k - 1.0))) for j in range(k)))
            if len(sel) != k:
                continue
            try:
                rk = occ_loft([sections[j] for j in sel], cap=True, ruled=False)
                Vk, Ak = volume_of(rk), area_of(rk)
                dv = abs(Vk - V0) / V0
                da = abs(Ak - A0) / max(A0, 1e-9)
                tested_k.append([k, round(max(dv, da), 9)])
                if dv <= DEGEN_REL and da <= DEGEN_REL:
                    mink = k
                    break
            except Exception:
                tested_k.append([k, None])
        out['min_even_subset_reproducing'] = mink
        out['min_subset_devs'] = tested_k[:12]
        out['min_subset_truncated'] = bool(n > 14)
    except Exception as e:
        out['err'] = type(e).__name__ + ':' + str(e)[:40]
    return out


def measure_loft_call(cap, released_faces):
    """单次 loft: 声明 N vs 实测 N (raw 特征体 与 发布 brep 两个层次)."""
    sections = cap['sections']
    rec = dict(declared_n=len(sections), ruled=cap['ruled'], combine=str(cap['combine']))
    infos, axis, parallel = section_info(sections)
    rec.update(axis=[round(x, 6) for x in axis], sections_parallel=parallel,
               section_lengths=[i['len'] for i in infos][:16],
               n_identical_consecutive=sum(1 for a, b in zip(infos, infos[1:])
                                           if abs(a['len'] - b['len']) < 1e-9 and
                                           _norm(_sub(a['centroid'], b['centroid'])) < 1e-9))
    raw = cap['raw']
    if raw is None:
        rec.update(raw_ok=False, measured_n=None, no_candidate=True, why='raw_loft_failed')
        return rec
    rec['raw_ok'] = True
    caps, lat = loft_lateral_faces(raw, axis)
    rec.update(n_cap_faces=len(caps), n_lateral_faces=len(lat))
    meas = [measure_loft_face(f, axis) for f in lat]
    good = [m for m in meas if m.get('measurable')]
    rec['lateral_surface_types'] = dict(collections.Counter(m['surf'] for m in meas))
    rec['faces'] = [m for m in sorted(meas, key=lambda m: -m.get('area', 0))[:6]]
    if not good:
        rec.update(measured_n=None, no_candidate=True,
                   why='no_bspline_lateral_face(' + ','.join(sorted(set(m['surf'] for m in meas))) + ')')
    else:
        good.sort(key=lambda m: -m['area'])
        vals = [m['measured_n'] for m in good]
        rec.update(no_candidate=False, measured_n=good[0]['measured_n'],
                   measured_n_all=sorted(set(vals)), measured_n_max=max(vals),
                   n_lateral_bspline=len(good))
        rec['match'] = (rec['measured_n'] == rec['declared_n'])
        rec['match_any_face'] = (rec['declared_n'] in vals)
        rec['err_n'] = rec['measured_n'] - rec['declared_n']
    # 发布件层次: 找到与 raw 侧面几何重合的面
    if released_faces is not None and lat:
        lat_b = [(f, bbox_of(f, 1e-3)) for f in lat]
        matched = []
        for rf, rb in released_faces:
            for f, b in lat_b:
                if not bbox_overlap(rb, b):
                    continue
                ok, d = face_lies_on(rf, f)
                if ok:
                    matched.append(rf)
                    break
        rec['released_matched_faces'] = len(matched)
        sf, ntot = survival_fraction(lat, released_faces)
        rec['released_survival_frac'] = round(sf, 4) if sf is not None else None
        rec['released_survival_pts'] = ntot
        rm = [measure_loft_face(f, axis) for f in matched]
        rmg = [m for m in rm if m.get('measurable')]
        if rmg:
            rmg.sort(key=lambda m: -m['area'])
            rec['released_measured_n'] = rmg[0]['measured_n']
            rec['released_measured_n_all'] = sorted(set(m['measured_n'] for m in rmg))
            rec['released_match'] = (rec['released_measured_n'] == rec['declared_n'])
        else:
            rec['released_measured_n'] = None
            rec['released_match'] = False
            rec['released_why'] = 'no_measurable_matched_face' if matched else 'no_matched_face'
    return rec


# ============================================================ SWEEP 测量
def sweep_lateral_and_caps(raw, profiles, path_shape):
    """raw 扫掠体: 用 截面面 的 面积/周长 推 端盖面积; 侧面 = 全部面 - 端盖面.
    端盖判据: 平面面 且 面积 与 截面面面积 之差 < 1e-6 相对, 且 质心在路径端点附近."""
    prof_area = 0.0
    prof_perim = 0.0
    for f in profiles:
        sh = f.wrapped if hasattr(f, 'wrapped') else f
        prof_area += area_of(sh)
        prof_perim += length_of(sh)   # 面的线性属性 = 全部边界边长之和
    return prof_area, prof_perim


def path_endpoints(path_shape):
    pts = sample_wire(path_shape, 2)
    if not pts:
        return None, None
    return pts[0], pts[-1]


def path_tangent_near(path_shape, pt):
    """路径上离 pt 最近的端点处的单位切向."""
    best = None
    ex = TopExp_Explorer(TS(path_shape), TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge_s(ex.Current())
        try:
            ad = BRepAdaptor_Curve(e)
            for t in (ad.FirstParameter(), ad.LastParameter()):
                p = gp_Pnt()
                d = ad.DN(t, 1)
                p = ad.Value(t)
                q = (p.X(), p.Y(), p.Z())
                dist = _norm(_sub(q, pt)) if pt else 0.0
                v = _unit((d.X(), d.Y(), d.Z()))
                if best is None or dist < best[0]:
                    best = (dist, v)
        except Exception:
            pass
        ex.Next()
    return best[1] if best else None


def profile_normal(face):
    sh = TS(face)
    ad = BRepAdaptor_Surface(sh)
    if ad.GetType() != GeomAbs_Plane:
        return None
    d = ad.Plane().Axis().Direction()
    return (d.X(), d.Y(), d.Z())


def measure_sweep_call(cap, released_faces):
    rec = dict(n_profiles=len(cap['profiles']), multisection=cap['multisection'],
               makeSolid=cap['makeSolid'], isFrenet=cap['isFrenet'], transition=str(cap['transition']))
    p = cap['path']
    ps = p.wrapped if hasattr(p, 'wrapped') else p
    if ps is None:
        rec.update(declared_len=None, why='no_path_shape')
        return rec
    try:
        Ld = length_of(ps)
    except Exception:
        Ld = None
    rec['declared_len'] = round(Ld, 9) if Ld else None
    try:
        closed = bool(BRepTools.OuterWire_s) and False
    except Exception:
        closed = False
    # 路径是否闭合: 首尾点重合
    a, b = path_endpoints(ps)
    rec['path_closed'] = bool(a and b and _norm(_sub(a, b)) < 1e-7)
    prof_area, prof_perim = sweep_lateral_and_caps(cap['raw'], cap['profiles'], ps)
    rec.update(profile_area=round(prof_area, 6), profile_perimeter=round(prof_perim, 6))
    raw = cap['raw']
    raw_sh = raw.wrapped if hasattr(raw, 'wrapped') else raw
    if raw_sh is None:
        rec.update(measured_len=None, no_candidate=True, why='raw_sweep_failed')
        return rec
    A = area_of(raw_sh)
    V = volume_of(raw_sh)
    rec.update(raw_area=round(A, 6), raw_volume=round(V, 6), raw_faces=len(faces_of(raw_sh)))
    n_caps = 0 if (rec['path_closed'] or not cap['makeSolid']) else 2
    rec['n_caps_assumed'] = n_caps
    if prof_perim > 1e-9:
        rec['L_area'] = round((A - n_caps * prof_area) / prof_perim, 9)
    if prof_area > 1e-9:
        rec['L_vol'] = round(V / prof_area, 9)
    # 截面是否垂直于路径 (不垂直 = 斜掠, Pappus 量到的是投影长度)
    cosang = None
    try:
        cs = []
        for f in cap['profiles']:
            n = profile_normal(f)
            if n is None:
                continue
            c = centroid_linear(f)
            t = path_tangent_near(ps, c)
            if t is None:
                continue
            cs.append(abs(_dot(_unit(n), t)))
        if cs:
            cosang = sum(cs) / len(cs)
    except Exception:
        cosang = None
    rec['profile_path_cos'] = round(cosang, 6) if cosang is not None else None
    rec['profile_perp_to_path'] = bool(cosang is not None and cosang >= 0.999)
    # 截面形心是否落在路径上 (Pappus 量的是"形心走过的长度", 形心不在路径上时它 != 路径长)
    offs = []
    for f in cap['profiles']:
        try:
            c = centroid_surface(f)
            v = BRepBuilderAPI_MakeVertex(gp_Pnt(*c)).Vertex()
            dd = shape_dist(v, ps)
            if dd is not None:
                offs.append(dd)
        except Exception:
            pass
    rec['profile_centroid_offset'] = round(max(offs), 6) if offs else None
    rec['profile_centroid_on_path'] = bool(offs and max(offs) <= 1e-6)
    rec['canonical_pipe'] = bool(rec['profile_perp_to_path'] and rec['profile_centroid_on_path']
                                 and not rec['path_closed'] and rec['n_profiles'] == 1
                                 and not cap['multisection'])
    if cosang and cosang > 1e-3 and rec.get('L_vol') is not None:
        rec['L_vol_oblique'] = round(rec['L_vol'] / cosang, 9)
    # 沿扫掠方向等参线长度 (区间校验): 取 非平面盖 的面, 用参数框内等参线
    iso = []
    for f in faces_of(raw_sh):
        surf = surface_of(f)
        u0, u1, v0, v1 = face_uv(f)
        if not all(map(math.isfinite, (u0, u1, v0, v1))):
            continue
        lu = iso_length(surf, True, (u0 + u1) / 2, v0, v1)
        lv = iso_length(surf, False, (v0 + v1) / 2, u0, u1)
        for L in (lu, lv):
            if L and L > 1e-9:
                iso.append(L)
    if iso and Ld:
        rec['iso_len_min'] = round(min(iso), 6)
        rec['iso_len_max'] = round(max(iso), 6)
        rec['declared_in_iso_range'] = bool(min(iso) - 1e-6 <= Ld <= max(iso) + 1e-6)
    # 主估计量: 截面垂直于路径时用 侧面积/周长; 斜掠时用 体积/(截面积*cos) (斜棱柱体积公式)
    if rec['profile_perp_to_path'] or rec.get('L_vol_oblique') is None:
        rec['estimator'] = 'L_area'
        rec['measured_len'] = rec.get('L_area')
    else:
        rec['estimator'] = 'L_vol_oblique'
        rec['measured_len'] = rec.get('L_vol_oblique')
    rec['no_candidate'] = rec.get('measured_len') is None
    if Ld and rec.get('measured_len') is not None and Ld > 1e-9:
        rec['rel_err_area'] = round(abs(rec['measured_len'] - Ld) / Ld, 9)
        rec['abs_err_area'] = round(abs(rec['measured_len'] - Ld), 9)
        rec['match'] = (rec['rel_err_area'] <= REL_EXACT)
        rec['close'] = (rec['rel_err_area'] <= REL_CLOSE or rec['abs_err_area'] <= ABS_CLOSE)
    if Ld and rec.get('L_vol') is not None and Ld > 1e-9:
        rec['rel_err_vol'] = round(abs(rec['L_vol'] - Ld) / Ld, 9)
    # 发布件层次
    if released_faces is not None:
        raw_faces = faces_of(raw_sh)
        # 侧面 = 排除 面积等于截面面积 的平面 (端盖)
        lat = []
        for f in raw_faces:
            ad = BRepAdaptor_Surface(f)
            if ad.GetType() == GeomAbs_Plane and abs(area_of(f) - prof_area) <= 1e-7 * max(1.0, prof_area):
                continue
            lat.append(f)
        lat_b = [(f, bbox_of(f, 1e-3)) for f in lat]
        A_match = 0.0
        n_match = 0
        for rf, rb in released_faces:
            for f, b in lat_b:
                if not bbox_overlap(rb, b):
                    continue
                ok, d = face_lies_on(rf, f)
                if ok:
                    A_match += area_of(rf)
                    n_match += 1
                    break
        A_lat_raw = sum(area_of(f) for f in lat)
        sf, ntot = survival_fraction(lat, released_faces)
        rec['released_survival_frac'] = round(sf, 4) if sf is not None else None
        rec['released_survival_pts'] = ntot
        rec['released_matched_faces'] = n_match
        rec['released_matched_area'] = round(A_match, 6)
        rec['raw_lateral_area'] = round(A_lat_raw, 6)
        rec['released_area_frac'] = round(A_match / A_lat_raw, 6) if A_lat_raw > 1e-9 else None
        rec['released_overmatched'] = bool(rec['released_area_frac'] is not None
                                           and rec['released_area_frac'] > 1.001)
        if prof_perim > 1e-9:
            rec['released_L_area'] = round(A_match / prof_perim, 9)
            if Ld and Ld > 1e-9:
                rec['released_rel_err'] = round(abs(rec['released_L_area'] - Ld) / Ld, 9)
                rec['released_match'] = (rec['released_rel_err'] <= REL_EXACT)
                rec['released_close'] = (rec['released_rel_err'] <= REL_CLOSE)
    return rec


# ============================================================ 单模型
def read_brep(path):
    shape = TopoDS_Shape()
    if not BRepTools.Read_s(shape, path, BRep_Builder()):
        return None
    return shape


def run(uuid, want_loft, want_sweep):
    py = os.path.join(OUT, uuid, 'cadquery.py')
    br = os.path.join(OUT, uuid, 'model.brep')
    if not (os.path.isfile(py) and os.path.isfile(br)):
        return dict(uuid=uuid, error='missing_files')
    rec = dict(uuid=uuid, has_loft=want_loft, has_sweep=want_sweep)
    t0 = time.time()
    try:
        src, g, dt = exec_program(py)
        rec.update(exec_ok=True, exec_s=round(dt, 3))
    except BaseException as e:
        return dict(uuid=uuid, has_loft=want_loft, has_sweep=want_sweep, exec_ok=False,
                    error='exec:' + type(e).__name__, exec_msg=str(e)[:100])
    # 静态求解 (sweep path)
    if want_sweep:
        try:
            rec['static_sweep'] = static_sweep_paths(src)
        except Exception as e:
            rec['static_sweep'] = [dict(ok=False, reason='static_fatal:' + type(e).__name__)]
    shape = read_brep(br)
    released = None
    if shape is not None:
        rf = faces_of(shape)
        released = [(f, bbox_of(f, 1e-3)) for f in rf]
        rec['released_faces'] = len(rf)
        try:
            fs = final_shape(g)
            if fs is not None:
                v1, v2 = volume_of(fs), volume_of(shape)
                rec['exec_vs_brep_rel_dvol'] = round(abs(v1 - v2) / max(abs(v2), 1e-9), 8)
        except Exception:
            pass
    else:
        rec['released_faces'] = None
    rec['n_loft_calls'] = len(CAPTURED['loft'])
    rec['n_sweep_calls'] = len(CAPTURED['sweep'])
    lofts, sweeps = [], []
    for cap in CAPTURED['loft']:
        try:
            m = measure_loft_call(cap, released)
        except Exception as e:
            m = dict(error='loft_measure:' + type(e).__name__ + ':' + str(e)[:60])
        try:
            if cap['raw'] is not None and len(cap['sections']) >= 3:
                m['degeneracy'] = loft_degeneracy([s for s in cap['sections']], cap['raw'])
        except Exception as e:
            m['degeneracy'] = dict(err=type(e).__name__)
        lofts.append(m)
    for i, cap in enumerate(CAPTURED['sweep']):
        try:
            m = measure_sweep_call(cap, released)
        except Exception as e:
            m = dict(error='sweep_measure:' + type(e).__name__ + ':' + str(e)[:60])
        st = rec.get('static_sweep') or []
        if i < len(st):
            m['static_ok'] = bool(st[i].get('ok'))
            m['static_reason'] = st[i].get('reason')
            m['static_len'] = st[i].get('path_len')
            m['static_how'] = st[i].get('how')
            if m.get('static_len') and m.get('declared_len'):
                m['static_vs_dynamic_rel'] = round(
                    abs(m['static_len'] - m['declared_len']) / m['declared_len'], 9)
        else:
            m['static_ok'] = None
            m['static_reason'] = 'call_count_mismatch'
        sweeps.append(m)
    rec['lofts'] = lofts
    rec['sweeps'] = sweeps
    rec['t_s'] = round(time.time() - t0, 2)
    # 释放引用
    CAPTURED['loft'] = []
    CAPTURED['sweep'] = []
    return rec


# ============================================================ worker / parent
def worker_main(listfile):
    install_hooks()
    items = [l.split() for l in open(listfile, encoding='utf-8') if l.strip()]
    for parts in items:
        u = parts[0]
        wl = parts[1] == '1'
        ws = parts[2] == '1'
        try:
            r = run(u, wl, ws)
        except BaseException as e:
            r = dict(uuid=u, has_loft=wl, has_sweep=ws, error='fatal:' + type(e).__name__ + ':' + str(e)[:80])
        sys.stdout.write('@@R@@' + json.dumps(r) + '\n')
        sys.stdout.flush()
    sys.stdout.write('@@END@@\n')
    sys.stdout.flush()


def run_chunk(items, mem_gb=4.0, per_item_timeout=180):
    import psutil
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8') as f:
        for u, wl, ws in items:
            f.write('%s %d %d\n' % (u, wl, ws))
        lf = f.name
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    p = subprocess.Popen([sys.executable, '-X', 'utf8', os.path.abspath(__file__), '--worker', lf],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                         encoding='utf-8', errors='replace', bufsize=1, env=env)
    out, reason, lines = {}, None, []

    def reader():
        for line in p.stdout:
            lines.append(line)
    th = threading.Thread(target=reader, daemon=True)
    th.start()
    ps = psutil.Process(p.pid)
    last = time.time()
    consumed = 0
    try:
        while True:
            while consumed < len(lines):
                line = lines[consumed]
                consumed += 1
                if line.startswith('@@R@@'):
                    r = json.loads(line[5:])
                    out[r['uuid']] = r
                    last = time.time()
            if p.poll() is not None and not th.is_alive():
                break
            try:
                if ps.memory_info().rss / 2 ** 30 > mem_gb:
                    reason = 'memory>%.1fGB' % mem_gb
                    p.kill()
                    break
            except Exception:
                pass
            if time.time() - last > per_item_timeout:
                reason = 'timeout'
                p.kill()
                break
            time.sleep(0.05)
        th.join(timeout=5)
        while consumed < len(lines):
            line = lines[consumed]
            consumed += 1
            if line.startswith('@@R@@'):
                r = json.loads(line[5:])
                out[r['uuid']] = r
    finally:
        try:
            os.remove(lf)
        except OSError:
            pass
        if p.poll() is None:
            p.kill()
    return out, reason


def drive(items, statefile, chunk=6, log=None):
    done = {}
    if os.path.isfile(statefile):
        for l in open(statefile, encoding='utf-8'):
            l = l.strip()
            if l:
                try:
                    r = json.loads(l)
                    done[r['uuid']] = r
                except Exception:
                    pass
    todo = [it for it in items if it[0] not in done]
    fo = open(statefile, 'a', encoding='utf-8')
    t0 = time.time()
    i = 0
    while i < len(todo):
        ch = todo[i:i + chunk]
        res, reason = run_chunk(ch)
        for u, wl, ws in ch:
            if u in res:
                done[u] = res[u]
                fo.write(json.dumps(res[u]) + '\n')
        fo.flush()
        missing = [it for it in ch if it[0] not in res]
        if missing and reason:
            u0 = missing[0]
            r1, reason1 = run_chunk([u0], per_item_timeout=240)
            rr = r1.get(u0[0], dict(uuid=u0[0], has_loft=u0[1], has_sweep=u0[2],
                                    error='killed:' + (reason1 or reason)))
            done[u0[0]] = rr
            fo.write(json.dumps(rr) + '\n')
            fo.flush()
            for it in missing[1:]:
                todo.insert(i + chunk, it)
        elif missing:
            for it in missing:
                rr = dict(uuid=it[0], has_loft=it[1], has_sweep=it[2], error='no_result')
                done[it[0]] = rr
                fo.write(json.dumps(rr) + '\n')
            fo.flush()
        i += chunk
        msg = '[%5.0fs] %d/%d done' % (time.time() - t0, min(i, len(todo)), len(todo))
        print(msg, flush=True)
        if log:
            log.write(msg + '\n')
            log.flush()
    fo.close()
    return [done[it[0]] for it in items if it[0] in done]


# ============================================================ 汇总
def dist(values, edges):
    values = sorted(v for v in values if v is not None)
    out = collections.OrderedDict()
    labels = ['[%g,%g)' % (edges[i], edges[i + 1]) for i in range(len(edges) - 1)] + ['>=%g' % edges[-1]]
    for lab in labels:
        out[lab] = 0
    for v in values:
        placed = False
        for i in range(len(edges) - 1):
            if edges[i] <= v < edges[i + 1]:
                out[labels[i]] += 1
                placed = True
                break
        if not placed:
            out[labels[-1]] += 1
    stats = dict(n=len(values))
    if values:
        stats.update(min=values[0], p50=values[len(values) // 2],
                     p95=values[min(len(values) - 1, int(0.95 * len(values)))], max=values[-1],
                     mean=round(sum(values) / len(values), 9))
    return dict(bins=out, stats=stats)


def summarize_loft(recs):
    S = collections.Counter()
    attrib = collections.Counter()
    by_n = collections.defaultdict(lambda: [0, 0])     # declared_n -> [measured, matched]
    err_n, examples, why = [], [], collections.Counter()
    declared_hist, measured_hist = collections.Counter(), collections.Counter()
    deg2 = invis = deg_tested = 0
    mink_eq_measured = mink_lt_declared = mink_known = 0
    mink_vs_measured = collections.Counter()
    surf_types = collections.Counter()
    lsurv = []
    rel_models = set()
    for r in recs:
        if not r.get('has_loft') or r.get('error'):
            continue
        for c in r.get('lofts', []):
            if c.get('error'):
                S['measure_error'] += 1
                continue
            S['attempted'] += 1
            rel_models.add(r['uuid'])
            declared_hist[c['declared_n']] += 1
            if c.get('ruled'):
                S['ruled_true'] += 1
            for t, n in (c.get('lateral_surface_types') or {}).items():
                surf_types[t] += n
            if c.get('no_candidate'):
                S['no_candidate'] += 1
                why[c.get('why', '?')] += 1
                continue
            S['measured'] += 1
            measured_hist[c['measured_n']] += 1
            by_n[c['declared_n']][0] += 1
            d = c.get('degeneracy') or {}
            if c.get('match'):
                S['matched'] += 1
                by_n[c['declared_n']][1] += 1
                if c['declared_n'] == 2:
                    S['matched_trivial_n2'] += 1
            else:
                S['mismatched'] += 1
                mk = d.get('min_even_subset_reproducing')
                if c['measured_n'] < c['declared_n']:
                    if mk is not None and mk < c['declared_n'] and mk == c['measured_n']:
                        attrib['A_declared_N_is_redundant:identical_solid_from_%s_sections,measurer_returns_exactly_that' % 'k'] += 1
                    elif mk is not None and mk < c['declared_n']:
                        attrib['B_declared_N_is_redundant(identical_solid_from_fewer_sections)_but_measured_k_differs'] += 1
                    elif (d.get('drop_one_invisible') or 0) > 0:
                        attrib['C_some_interior_sections_leave_no_trace_in_the_solid'] += 1
                    else:
                        attrib['D_sections_all_visible_but_approximation_collapsed(fewer_poles_than_sections)'] += 1
                else:
                    attrib['E_approximation_needed_more_poles_than_sections'] += 1
                if len(examples) < 40:
                    examples.append(dict(uuid=r['uuid'], declared_n=c['declared_n'],
                                         measured_n=c['measured_n'], err=c.get('err_n'),
                                         lateral=c.get('lateral_surface_types'),
                                         faces=c.get('faces', [])[:2],
                                         degenerate_to_2=(c.get('degeneracy') or {}).get('degenerate_to_2'),
                                         min_even_subset=(c.get('degeneracy') or {}).get('min_even_subset_reproducing'),
                                         drop_one_invisible=(c.get('degeneracy') or {}).get('drop_one_invisible')))
            if c.get('match_any_face'):
                S['matched_on_some_face'] += 1
            err_n.append(c.get('err_n'))
            if c.get('released_survival_frac') is not None:
                lsurv.append(c['released_survival_frac'])
                if c['released_survival_frac'] >= 0.999:
                    S['released_surface_fully_on_boundary'] += 1
                elif c['released_survival_frac'] <= 1e-9:
                    S['released_surface_gone'] += 1
            if c.get('released_measured_n') is not None:
                S['released_measured'] += 1
                if c.get('released_match'):
                    S['released_matched'] += 1
            elif 'released_measured_n' in c:
                S['released_no_candidate'] += 1
            if d.get('tested'):
                deg_tested += 1
                if d.get('degenerate_to_2'):
                    deg2 += 1
                invis += d.get('drop_one_invisible', 0) or 0
            mk = d.get('min_even_subset_reproducing')
            if mk is not None:
                mink_known += 1
                if mk < c['declared_n']:
                    mink_lt_declared += 1
                if mk == c.get('measured_n'):
                    mink_eq_measured += 1
                mink_vs_measured[int(c.get('measured_n', 0)) - int(mk)] += 1
    return dict(
        counts=dict(S),
        models=len(rel_models),
        declared_n_hist=dict(sorted(declared_hist.items())),
        measured_n_hist=dict(sorted(measured_hist.items())),
        lateral_surface_types=dict(surf_types.most_common()),
        err_n_hist=dict(sorted(collections.Counter(e for e in err_n if e is not None).items())),
        err_n_abs_dist=dist([abs(e) for e in err_n if e is not None], [0, 1, 2, 3, 5, 10]),
        no_candidate_reasons=dict(why.most_common()),
        released_surface_survival_dist=dist(lsurv, [0, 1e-9, 0.5, 0.9, 0.99, 0.999, 1.0]),
        mismatch_attribution=dict(attrib.most_common()),
        by_declared_n=dict((k, dict(measured=v[0], matched=v[1],
                                    pct=round(100.0 * v[1] / v[0], 1) if v[0] else None))
                           for k, v in sorted(by_n.items())),
        degeneracy=dict(tested_calls=deg_tested, degenerate_to_two_sections=deg2,
                        sum_invisible_interior_sections=invis,
                        min_subset_tested_calls=mink_known,
                        min_even_subset_smaller_than_declared=mink_lt_declared,
                        measured_n_equals_min_subset=mink_eq_measured,
                        measured_minus_min_subset_hist=dict(sorted(mink_vs_measured.items()))),
        match_rate_pct=round(100.0 * S['matched'] / S['measured'], 3) if S['measured'] else None,
        match_rate_pct_of_attempted=round(100.0 * S['matched'] / S['attempted'], 3) if S['attempted'] else None,
        released_match_rate_pct=round(100.0 * S['released_matched'] / S['released_measured'], 3)
        if S['released_measured'] else None,
        mismatch_examples=examples,
    )


def summarize_sweep(recs, subset='all sweep calls', pred=lambda c: True):
    S = collections.Counter()
    attrib = collections.Counter()
    rel_attrib = collections.Counter()
    rel_area, rel_vol, rel_static = [], [], []
    static_reasons = collections.Counter()
    examples = []
    rel_models = set()
    released_frac = []
    surv = []
    for r in recs:
        if not r.get('has_sweep') or r.get('error'):
            continue
        for c in r.get('sweeps', []):
            if c.get('error'):
                S['measure_error'] += 1
                continue
            if not pred(c):
                continue
            S['attempted'] += 1
            rel_models.add(r['uuid'])
            if c.get('canonical_pipe'):
                S['canonical_pipe'] += 1
            if c.get('static_ok'):
                S['statically_resolvable'] += 1
                if c.get('static_vs_dynamic_rel') is not None:
                    rel_static.append(c['static_vs_dynamic_rel'])
                    if c['static_vs_dynamic_rel'] <= REL_CLOSE:
                        S['static_agrees_with_replay'] += 1
            else:
                S['not_statically_resolvable'] += 1
                static_reasons[str(c.get('static_reason', '?')).split(':')[0]] += 1
            if c.get('declared_len') is None:
                S['no_declared_len'] += 1
                continue
            S['declared_ok'] += 1
            if c.get('no_candidate') or c.get('measured_len') is None:
                S['no_candidate'] += 1
                continue
            S['measured'] += 1
            e = c.get('rel_err_area')
            rel_area.append(e)
            if c.get('rel_err_vol') is not None:
                rel_vol.append(c['rel_err_vol'])
            S['estimator_' + str(c.get('estimator'))] += 1
            if c.get('profile_perp_to_path'):
                S['profile_perpendicular_to_path'] += 1
            else:
                S['profile_oblique_to_path'] += 1
            if (c.get('L_vol') is not None and c.get('L_area') is not None
                    and abs(c['L_vol'] - c['L_area']) <= 1e-6 * max(1.0, abs(c['L_area']))):
                S['two_estimators_agree'] += 1
            if c.get('match'):
                S['matched_exact'] += 1
            elif c.get('close'):
                S['matched_close'] += 1
            elif e is not None and e <= 0.01:
                S['matched_loose_1pct'] += 1
            if c.get('match') or c.get('close'):
                pass
            else:
                S['mismatched'] += 1
                if c.get('profile_path_cos') is not None and c['profile_path_cos'] < 0.01:
                    attrib['A0_profile_plane_contains_path_direction(degenerate_sweep)'] += 1
                elif not c.get('profile_centroid_on_path'):
                    attrib['A1_profile_centroid_off_the_path(Pappus_measures_centroid_travel)'] += 1
                elif not c.get('profile_perp_to_path'):
                    attrib['A2_profile_not_perpendicular_to_path(oblique_sweep)'] += 1
                elif c.get('path_closed'):
                    attrib['B_closed_path(no_caps)'] += 1
                elif str(c.get('transition')) == 'round':
                    attrib['C_round_transition_adds_corner_material'] += 1
                elif c.get('n_profiles', 1) > 1 or c.get('multisection'):
                    attrib['D_multi_profile_or_multisection'] += 1
                else:
                    attrib['E_other'] += 1
                if len(examples) < 40:
                    examples.append(dict(uuid=r['uuid'], declared=c.get('declared_len'),
                                         L_area=c.get('L_area'), L_vol=c.get('L_vol'),
                                         rel_err=e, transition=c.get('transition'),
                                         isFrenet=c.get('isFrenet'), n_profiles=c.get('n_profiles'),
                                         path_closed=c.get('path_closed'),
                                         iso_min=c.get('iso_len_min'), iso_max=c.get('iso_len_max'),
                                         in_iso_range=c.get('declared_in_iso_range')))
            if c.get('declared_in_iso_range'):
                S['declared_within_iso_range'] += 1
            if c.get('released_survival_frac') is not None:
                surv.append(c['released_survival_frac'])
                if c['released_survival_frac'] >= 0.999:
                    S['released_surface_fully_on_boundary'] += 1
                elif c['released_survival_frac'] <= 1e-9:
                    S['released_surface_gone'] += 1
            if c.get('released_overmatched'):
                S['released_area_overmatched'] += 1
            if c.get('released_L_area') is not None:
                S['released_measured'] += 1
                released_frac.append(c.get('released_area_frac'))
                if c.get('released_match'):
                    S['released_matched_exact'] += 1
                elif c.get('released_close'):
                    S['released_matched_close'] += 1
                fr = c.get('released_area_frac')
                if fr is None:
                    rel_attrib['unknown'] += 1
                elif fr <= 1e-9:
                    rel_attrib['A_swept_faces_fully_consumed_by_later_boolean'] += 1
                elif fr < 0.999:
                    rel_attrib['B_swept_faces_partially_trimmed'] += 1
                elif c.get('released_close'):
                    rel_attrib['C_intact_and_recovered'] += 1
                else:
                    rel_attrib['D_intact_but_length_off'] += 1
    meas = S['measured']
    return dict(
        subset=subset,
        counts=dict(S),
        models=len(rel_models),
        static_not_resolvable_reasons=dict(static_reasons.most_common()),
        mismatch_attribution=dict(attrib.most_common()),
        released_attribution=dict(rel_attrib.most_common()),
        static_vs_replay_rel_dist=dist(rel_static, [0, 1e-9, 1e-6, 1e-3, 1e-2, 1]),
        rel_err_area_dist=dist(rel_area, [0, 1e-9, 1e-6, 1e-4, 1e-3, 1e-2, 0.1, 1]),
        rel_err_vol_dist=dist(rel_vol, [0, 1e-9, 1e-6, 1e-4, 1e-3, 1e-2, 0.1, 1]),
        released_area_fraction_dist=dist([f for f in released_frac if f is not None and f <= 1.001],
                                         [0, 0.5, 0.9, 0.99, 0.999, 1.0]),
        released_surface_survival_dist=dist(surv, [0, 1e-9, 0.5, 0.9, 0.99, 0.999, 1.0]),
        match_rate_exact_pct=round(100.0 * S['matched_exact'] / meas, 3) if meas else None,
        match_rate_close_pct=round(100.0 * (S['matched_exact'] + S['matched_close']) / meas, 3) if meas else None,
        match_rate_1pct_pct=round(100.0 * (S['matched_exact'] + S['matched_close'] + S['matched_loose_1pct'])
                                  / meas, 3) if meas else None,
        released_match_close_pct=round(100.0 * (S['released_matched_exact'] + S['released_matched_close'])
                                       / S['released_measured'], 3) if S['released_measured'] else None,
        mismatch_examples=examples,
    )


def build_lists():
    """扫描语料, 找出含 .loft( / .sweep( 的模型."""
    lofts, sweeps = [], []
    for name in sorted(os.listdir(OUT)):
        py = os.path.join(OUT, name, 'cadquery.py')
        if not os.path.isfile(py):
            continue
        try:
            s = open(py, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        if '.loft(' in s:
            lofts.append(name)
        if '.sweep(' in s:
            sweeps.append(name)
    return lofts, sweeps


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == '--worker':
        worker_main(args[1])
        sys.exit(0)
    sample, seed, limit, chunk = 0, 42, 0, 6
    statefile = os.path.join(tempfile.gettempdir(), 'exp_w3_partial.jsonl')
    listcache = os.path.join(tempfile.gettempdir(), 'exp_w3_lists.json')
    i = 0
    while i < len(args):
        if args[i] == '--sample':
            sample = int(args[i + 1]); i += 2
        elif args[i] == '--seed':
            seed = int(args[i + 1]); i += 2
        elif args[i] == '--limit':
            limit = int(args[i + 1]); i += 2
        elif args[i] == '--chunk':
            chunk = int(args[i + 1]); i += 2
        elif args[i] == '--state':
            statefile = args[i + 1]; i += 2
        elif args[i] == '--lists':
            listcache = args[i + 1]; i += 2
        else:
            i += 1
    t0 = time.time()
    if os.path.isfile(listcache):
        d = json.load(open(listcache, encoding='utf-8'))
        lofts, sweeps = d['loft'], d['sweep']
    else:
        lofts, sweeps = build_lists()
        json.dump(dict(loft=lofts, sweep=sweeps), open(listcache, 'w', encoding='utf-8'))
    pop_loft, pop_sweep = len(lofts), len(sweeps)
    if sample:
        random.seed(seed)
        lofts = sorted(random.sample(lofts, min(sample, len(lofts))))
        sweeps = sorted(random.sample(sweeps, min(sample, len(sweeps))))
    sl, ss = set(lofts), set(sweeps)
    items = [(u, u in sl, u in ss) for u in sorted(sl | ss)]
    if limit:
        items = items[:limit]
    log = open(os.path.join(REV_DIR, 'exp_w3_run.log'), 'a', encoding='utf-8')
    log.write('=== start %s  models=%d (loft=%d sweep=%d, population %d/%d)\n'
              % (time.strftime('%Y-%m-%d %H:%M:%S'), len(items), len(sl), len(ss), pop_loft, pop_sweep))
    recs = drive(items, statefile, chunk=chunk, log=log)
    with open(os.path.join(REV_DIR, 'exp_w3_loft_sweep_records.jsonl'), 'w', encoding='utf-8') as fo:
        for r in recs:
            fo.write(json.dumps(r) + '\n')
    errs = collections.Counter(str(r.get('error', '')).split(':')[0] for r in recs if r.get('error'))
    summary = dict(
        population=dict(models_with_loft=pop_loft, models_with_sweep=pop_sweep, corpus_models=10000),
        sample=dict(n_models=len(items), n_loft_models=len(sl), n_sweep_models=len(ss),
                    seed=(seed if sample else None), sampled=bool(sample)),
        tolerances=dict(rel_exact=REL_EXACT, rel_close=REL_CLOSE, abs_close_mm=ABS_CLOSE,
                        face_match_tol_mm=GEO_TOL, degeneracy_rel=DEGEN_REL),
        errors=dict(errs.most_common()),
        n_models_ok=sum(1 for r in recs if not r.get('error')),
        exec_vs_released_brep_rel_dvol=dist([r.get('exec_vs_brep_rel_dvol') for r in recs
                                             if r.get('exec_vs_brep_rel_dvol') is not None],
                                            [0, 1e-9, 1e-6, 1e-4, 1e-2, 1]),
        loft=summarize_loft(recs),
        sweep=summarize_sweep(recs),
        sweep_canonical_pipe=summarize_sweep(
            recs, 'canonical pipe: single profile, profile plane perpendicular to the path and profile '
                  'centroid on the path, open path', lambda c: bool(c.get('canonical_pipe'))),
        sweep_non_canonical=summarize_sweep(recs, 'all other sweeps',
                                            lambda c: not c.get('canonical_pipe')),
        runtime_s=round(time.time() - t0, 1),
    )
    json.dump(summary, open(os.path.join(REV_DIR, 'exp_w3_loft_sweep.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    log.write('=== done %.1fs\n' % (time.time() - t0))
    log.close()
    print(json.dumps(summary, indent=1, ensure_ascii=False)[:6000])
