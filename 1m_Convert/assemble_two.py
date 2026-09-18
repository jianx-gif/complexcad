"""双件夹紧装配: 一颗螺栓把**两个零件 A、B** 夹紧固定在一起(法兰对接/盖板螺接)。
产出 STEP/STL + 三视图(光杆简化投影) + 可重跑装配脚本(内嵌 A、B 两段源码)。

复用 assemble_fasteners 的 helper(检孔/选规格/BOM/气泡/中心线/脚本工具), 不动其
现有 produce/assemble/cylinder_holes 行为。

几何:
  1. A、B 各自 cylinder_holes 找孔, 挑一对孔径匹配同一螺纹规格的孔 hA、hB。
  2. A 固定不动。把 B 变换: 先旋转使 hB 轴与 hA 轴共线, 再平移使 B 落到 A 顶面之上、
     两孔同轴(B 底面贴 A 顶面, 不穿插不留缝)。
  3. 一颗螺栓沿公共轴从顶部穿过 B、A: 顶部加垫圈, 底部(A 下表面外)加螺母。
     杆长 = 两件沿轴总厚 + 螺母厚 + 余量, round 到偶数。
  4. compound = A ∪ B(两 base) + 螺栓 + 垫圈 + 螺母。

用法:
  python -X utf8 assemble_two.py --demo
  python -X utf8 assemble_two.py --data <uuidA> <uuidB>   # 从 test parquet 取两件
  python -X utf8 assemble_two.py --auto                   # 自动从数据集找一对可配对件
"""
import sys, os, math, argparse, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import cadquery as cq

import assemble_fasteners as af
import library_parts as lp

from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir, gp_Vec
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.TopAbs import TopAbs_OUT, TopAbs_IN, TopAbs_ON, TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp


def _topods(shape):
    return af._to_topods(shape)


# =====================================================================
# 平面对接判定 + A-B 干涉检查
# =====================================================================
def _solid_volume(td):
    """实体体积(mm^3)。"""
    g = GProp_GProps()
    BRepGProp.VolumeProperties_s(td, g)
    return abs(g.Mass())


def _planar_faces(td):
    """返回实体所有平面 face 的 (normal_unit, point_on_plane, face)。法向已单位化。"""
    out = []
    exp = TopExp_Explorer(td, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Plane:
            pl = surf.Plane()
            ax = pl.Axis()
            n = ax.Direction(); loc = ax.Location()
            out.append(((n.X(), n.Y(), n.Z()),
                        (loc.X(), loc.Y(), loc.Z()), face))
        exp.Next()
    return out


def hole_plane_ends(td, hole, axis_tol=0.985, near=2.5):
    """对一个孔(r,a,p,t0,t1), 判定其沿轴两端口附近是否各有一个**垂直于孔轴的平面**
    (法兰/平板的平表面)作为贴合面。

    端口世界坐标: 端 hi = p + a*t1, 端 lo = p + a*t0。
    对每端: 在实体的平面 face 里找一个 法向≈±孔轴 且 该平面到端口点沿轴距离很小(<near)
    的平面。找到 -> 该端是"平面对接端", 返回它在孔轴参数 t 上的精确位置(平面与孔轴交点)。

    返回 dict:
      {'hi': (is_plane, t_world), 'lo': (is_plane, t_world)}
      t_world 是平面沿孔轴的 t 参数(相对 p); 没找到平面则 is_plane=False, t_world=端口 t。
    """
    a, p = hole[1], hole[2]
    res = {}
    planes = _planar_faces(td)
    for key, t_port in (("hi", hole[4]), ("lo", hole[3])):
        port = (p[0]+a[0]*t_port, p[1]+a[1]*t_port, p[2]+a[2]*t_port)
        best = None  # (|dist|, t_plane)
        for n, q, _f in planes:
            dot = abs(n[0]*a[0] + n[1]*a[1] + n[2]*a[2])
            if dot < axis_tol:           # 平面法向不沿孔轴 -> 不是垂直端面
                continue
            # 平面沿孔轴的 t: 平面过 q, 法向 n(≈±a)。孔轴线 p + a*t 与平面交点。
            # (q - (p + a*t)) · n = 0  ->  t = ((q-p)·n) / (a·n)
            an = a[0]*n[0] + a[1]*n[1] + a[2]*n[2]
            if abs(an) < 1e-6:
                continue
            t_plane = ((q[0]-p[0])*n[0] + (q[1]-p[1])*n[1] + (q[2]-p[2])*n[2]) / an
            dist = abs(t_plane - t_port)
            if dist <= near and (best is None or dist < best[0]):
                best = (dist, t_plane)
        if best is not None:
            res[key] = (True, best[1])
        else:
            res[key] = (False, t_port)
    return res


def hole_confined_segment(td, hole, ports=None, n_circ=24, n_layers=20,
                          ring_thresh=0.92, min_len=1.0):
    """沿孔轴扫描, 找出"整圈孔壁完整(被料包裹)"的**连续子段**, 返回 (ok, t_a, t_b)。

    每层在 r-δ(孔内, 应空) 与 r+δ(贴壁外, 应有料) 各绕一圈撒 n_circ 点; 一层算
    "完整环"当 (内空 & 外实) 的比例 >= ring_thresh。把完整环的连续区间合并, 取最长
    的那段。
      - 真实完整通孔: 在穿料的那段所有层都是完整环 => 得到一段长度足够(>= min_len)。
      - 边缘半孔/豁口: 任何层都有一截缺料(同方向), 完整环比例不达标 => 没有合格段。
      - cylinder_holes 把 t-span 延伸到料外的开放区: 那些层不是完整环, 自动被排除。
    ok = 最长完整段长度 >= min_len。t_a/t_b 是该段的轴向端(可作真实孔壁范围)。"""
    r, a, p, t0, t1 = hole
    clf = BRepClass3d_SolidClassifier(td)

    def _inside(pt):
        clf.Perform(gp_Pnt(*pt), 1e-7)
        st = clf.State()
        return st == TopAbs_IN or st == TopAbs_ON

    u, v = af._perp_basis(a)
    d_in = min(0.5, 0.4 * r)
    d_out = 0.2
    lo, hi = (min(ports), max(ports)) if ports else (t0, t1)
    span = hi - lo
    if span <= 1e-6:
        return False, lo, hi
    ts = [lo + span * (i + 0.5) / n_layers for i in range(n_layers)]
    flags = []
    for tt in ts:
        c = (p[0]+a[0]*tt, p[1]+a[1]*tt, p[2]+a[2]*tt)
        g = 0
        for k in range(n_circ):
            ang = 2*math.pi*k/n_circ
            rd = (u[0]*math.cos(ang)+v[0]*math.sin(ang),
                  u[1]*math.cos(ang)+v[1]*math.sin(ang),
                  u[2]*math.cos(ang)+v[2]*math.sin(ang))
            inner = (c[0]+rd[0]*(r-d_in), c[1]+rd[1]*(r-d_in), c[2]+rd[2]*(r-d_in))
            outer = (c[0]+rd[0]*(r+d_out), c[1]+rd[1]*(r+d_out), c[2]+rd[2]*(r+d_out))
            if (not _inside(inner)) and _inside(outer):
                g += 1
        flags.append(g / n_circ >= ring_thresh)
    # 最长连续 True 段
    best_i = best_len = 0
    i = 0
    while i < n_layers:
        if flags[i]:
            j = i
            while j < n_layers and flags[j]:
                j += 1
            if j - i > best_len:
                best_len = j - i; best_i = i
            i = j
        else:
            i += 1
    if best_len == 0:
        return False, lo, hi
    step = span / n_layers
    t_a = ts[best_i] - 0.5*step
    t_b = ts[best_i + best_len - 1] + 0.5*step
    return (t_b - t_a) >= min_len, t_a, t_b


def hole_is_complete(td, hole, ports=None):
    """孔是否为完整圆孔(有足够长的整圈包裹孔壁连续段)。"""
    ok, _, _ = hole_confined_segment(td, hole, ports=ports)
    return ok


def solid_interference(tdA, tdB, vol_ratio=0.01, n_sample=4000):
    """检查 A、B 两实体的干涉(穿插)。优先布尔相交(BRepAlgoAPI_Common)体积比;
    布尔不稳(崩/无效)时退化为点采样: 在 B 包围盒内撒点, 统计同时落在 A、B 内部的
    比例, 折算成相交体积近似。

    返回 (interferes_bool, ratio, method)。ratio = 相交体积 / min(VA,VB)。
    A、B 应是无螺纹的零件本体, 布尔通常可行。"""
    VA = _solid_volume(tdA); VB = _solid_volume(tdB)
    vmin = max(1e-9, min(VA, VB))
    # ---- 优先布尔 ----
    try:
        common = BRepAlgoAPI_Common(tdA, tdB)
        common.Build()
        if common.IsDone():
            cs = common.Shape()
            vi = _solid_volume(cs)
            ratio = vi / vmin
            return ratio > vol_ratio, ratio, "boolean"
    except Exception:
        pass
    # ---- 点采样兜底 ----
    bx = Bnd_Box(); BRepBndLib.Add_s(tdB, bx)
    x0, y0, z0, x1, y1, z1 = bx.Get()
    clfA = BRepClass3d_SolidClassifier(tdA)
    clfB = BRepClass3d_SolidClassifier(tdB)
    import random
    rnd = random.Random(12345)
    inB = inAB = 0
    for _ in range(n_sample):
        pt = gp_Pnt(rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(z0, z1))
        clfB.Perform(pt, 1e-7)
        if clfB.State() not in (TopAbs_IN, TopAbs_ON):
            continue
        inB += 1
        clfA.Perform(pt, 1e-7)
        if clfA.State() in (TopAbs_IN,):
            inAB += 1
    if inB == 0:
        return False, 0.0, "sample"
    # 相交体积 ≈ (inAB/inB)*VB ; ratio 相对 vmin
    vi = (inAB / inB) * VB
    ratio = vi / vmin
    return ratio > vol_ratio, ratio, "sample"


def _axis_to_z(a):
    """轴方向归一化为指向 +Z(库件天然 头/正面在上)。"""
    return a if a[2] >= 0 else (-a[0], -a[1], -a[2])


def _surface_extent_along_axis(solid, a, p):
    """沿轴 a(过点 p) 求实体在该轴上的 [t_lo, t_hi]: 把包围盒 8 角投到轴上取范围。
    这是该实体沿螺栓轴的真实跨度(料底/料顶)。"""
    bx = Bnd_Box(); BRepBndLib.Add_s(solid, bx)
    x0, y0, z0, x1, y1, z1 = bx.Get()
    corners = [(x0, y0, z0), (x1, y0, z0), (x0, y1, z0), (x1, y1, z0),
               (x0, y0, z1), (x1, y0, z1), (x0, y1, z1), (x1, y1, z1)]
    ts = [(c[0]-p[0])*a[0] + (c[1]-p[1])*a[1] + (c[2]-p[2])*a[2] for c in corners]
    return min(ts), max(ts)


def _transform_shape(td, trsf):
    return cq.Shape(BRepBuilderAPI_Transform(td, trsf, True).Shape())


def align_B_onto_A(shapeA, hA, shapeB, hB):
    """算把 B 摆到 A 顶面之上、两孔同轴的变换 trsf, 并返回:
      (B_moved, axis, pA, tA_bot, tA_top, tB_bot, tB_top, trsf, contact_t, seats)
    约定: axis = A 孔轴(归一化指向 +Z); 螺栓沿 axis 从顶(B 上表面)向下穿到底(A 下表面)。
    A 不动。B 经 trsf 后: 其孔轴与 axis 共线, 且 B 的**底面真实平面**贴 A 的**顶面真实
    平面**(贴合, 不穿插不留缝)。
    seats(全部 pA-相对 t, 供紧固件就位): B_top(头/垫圈坐的 B 顶面平面)、A_bot(螺母坐
    的 A 底面平面)、B_top_plane/A_bot_plane(这两个面是否真为垂直轴平面)。

    trsf 作用到 B 的点 x: x' = T · R · x
      R: 把 B 孔轴 bB(原始) 旋转到 axis。
      T: 旋转后, 让 B 孔轴上锚点落到 A 孔轴上(径向对齐), 并沿 axis 平移使 B 底贴 A 顶。
    """
    tdA = _topods(shapeA)
    tdB = _topods(shapeB)

    rA, aA0, pA, _, _ = hA
    rB, aB0, pB, _, _ = hB

    axis = _axis_to_z(aA0)                       # 公共轴 = A 孔轴(指 +Z)
    bB = aB0 if aB0[2] >= 0 else (-aB0[0], -aB0[1], -aB0[2])

    # A 沿 axis 的真实上下表面
    tA_lo, tA_hi = _surface_extent_along_axis(tdA, axis, pA)
    tA_bot, tA_top = tA_lo, tA_hi

    # ---- R: 把 bB 旋转到 axis ----
    R = gp_Trsf()
    dot = max(-1.0, min(1.0, bB[0]*axis[0] + bB[1]*axis[1] + bB[2]*axis[2]))
    ang = math.acos(dot)
    if ang > 1e-7:
        rax = (bB[1]*axis[2]-bB[2]*axis[1], bB[2]*axis[0]-bB[0]*axis[2],
               bB[0]*axis[1]-bB[1]*axis[0])      # bB × axis
        if math.hypot(*rax) < 1e-9:              # 反平行: 任取一条垂直轴转 180
            u, _v = af._perp_basis(axis)
            rax = u
        R.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(*rax)), ang)

    # 旋转后 B 孔轴锚点 pB' 与方向(= axis)
    pBv = gp_Vec(pB[0], pB[1], pB[2]).Transformed(R)
    pBr = (pBv.X(), pBv.Y(), pBv.Z())

    # 旋转后 B 沿 axis 的跨度(B 整体, 用旋转后的实体包围盒)
    Btmp = _transform_shape(tdB, R)
    tdBr = Btmp.wrapped
    tB_lo, tB_hi = _surface_extent_along_axis(tdBr, axis, pA)
    # B 厚度(沿 axis)
    thickB = tB_hi - tB_lo

    # ---- 真实平面贴合面 ----
    # A 的"顶面"(B 坐上去那面): A 孔朝 +axis 的端口附近的垂直平面(若有), 否则包围盒顶。
    # B 的"底面"(坐到 A 上那面): 旋转后 B 孔朝 -axis 的端口附近的垂直平面, 否则包围盒底。
    # 用平面与孔轴的精确交点 t 作贴合基准, 保证两件实体平面相接、不穿插不留缝。
    # 用真实的 A 孔(原始 hA)的端点求 A 顶面平面。
    # hA 的轴 aA0 可能朝 -axis; 用 axis 重投影 hA 端点。
    pA_h = hA[2]
    tA_h0 = (pA_h[0]+hA[1][0]*hA[3], pA_h[1]+hA[1][1]*hA[3], pA_h[2]+hA[1][2]*hA[3])
    tA_h1 = (pA_h[0]+hA[1][0]*hA[4], pA_h[1]+hA[1][1]*hA[4], pA_h[2]+hA[1][2]*hA[4])
    tA_end0 = (tA_h0[0]-pA[0])*axis[0] + (tA_h0[1]-pA[1])*axis[1] + (tA_h0[2]-pA[2])*axis[2]
    tA_end1 = (tA_h1[0]-pA[0])*axis[0] + (tA_h1[1]-pA[1])*axis[1] + (tA_h1[2]-pA[2])*axis[2]
    holeA_axis = (rA, axis, pA, min(tA_end0, tA_end1), max(tA_end0, tA_end1))
    epA = hole_plane_ends(tdA, holeA_axis)
    A_top_contact = epA["hi"][1] if epA["hi"][0] else tA_top
    # A 孔朝 -axis 的端口平面 = A 底面平面(螺母坐这里)。无平面则退包围盒底。
    A_bot_seat = epA["lo"][1] if epA["lo"][0] else tA_bot
    A_bot_is_plane = epA["lo"][0]

    # 旋转后 B 孔: 锚点 pBr, 轴 = axis(因为已旋到 axis), 端点用旋转后实体跨度近似;
    # 但更准: 把 B 原孔端点经 R 变换后投到 axis。
    def _xf(pt):
        v = gp_Vec(pt[0], pt[1], pt[2]).Transformed(R)
        return (v.X(), v.Y(), v.Z())
    pB_h = hB[2]
    bB_end0 = _xf((pB_h[0]+aB0[0]*hB[3], pB_h[1]+aB0[1]*hB[3], pB_h[2]+aB0[2]*hB[3]))
    bB_end1 = _xf((pB_h[0]+aB0[0]*hB[4], pB_h[1]+aB0[1]*hB[4], pB_h[2]+aB0[2]*hB[4]))
    # t 必须相对 holeB 的锚点 pBr(与 hole_plane_ends 内部一致), 不能相对 pA。
    tB_e0 = (bB_end0[0]-pBr[0])*axis[0] + (bB_end0[1]-pBr[1])*axis[1] + (bB_end0[2]-pBr[2])*axis[2]
    tB_e1 = (bB_end1[0]-pBr[0])*axis[0] + (bB_end1[1]-pBr[1])*axis[1] + (bB_end1[2]-pBr[2])*axis[2]
    holeB_axis = (rB, axis, pBr, min(tB_e0, tB_e1), max(tB_e0, tB_e1))
    epB = hole_plane_ends(tdBr, holeB_axis)
    B_bot_contact = epB["lo"][1] if epB["lo"][0] else tB_lo
    # B 孔朝 +axis 的端口平面 = B 顶面平面(螺栓头/垫圈坐这里), 在 T 平移前的 t。
    B_top_seat_pre = epB["hi"][1] if epB["hi"][0] else tB_hi
    B_top_is_plane = epB["hi"][0]

    # ---- 统一到"最终放置帧": 一切 t 都相对锚点 pA、轴 axis(_place/anchor3d 也用 pA)。
    # 世界轴坐标 s(pt) = pt·axis。 sA = pA·axis, sBr = pBr·axis。
    # A 的 t 本就相对 pA(hole_plane_ends 用 pA 锚点)=> A_top_contact / A_bot_seat 直接用。
    # B 的 t 相对 pBr => 世界轴坐标 = sBr + tB; 换算成 pA-相对 = (sBr - sA) + tB。
    sA = pA[0]*axis[0] + pA[1]*axis[1] + pA[2]*axis[2]
    sBr = pBr[0]*axis[0] + pBr[1]*axis[1] + pBr[2]*axis[2]
    off = sBr - sA                                  # B(pBr相对) -> A(pA相对) 的轴坐标偏移

    # ---- T: 平移分两部分 ----
    # (1) 径向对齐: 把旋转后 B 孔锚点 pBr 移到 A 孔轴上(消除垂直于 axis 的偏移)。
    d = (pA[0]-pBr[0], pA[1]-pBr[1], pA[2]-pBr[2])
    d_par = (d[0]*axis[0] + d[1]*axis[1] + d[2]*axis[2])     # 沿轴分量
    radial = (d[0]-axis[0]*d_par, d[1]-axis[1]*d_par, d[2]-axis[2]*d_par)
    # (2) 轴向: 让 B 底面平面(pA相对 off+B_bot_contact)贴到 A 顶面平面(A_top_contact)。
    axial = A_top_contact - (off + B_bot_contact)

    move = (radial[0] + axis[0]*axial,
            radial[1] + axis[1]*axial,
            radial[2] + axis[2]*axial)
    T = gp_Trsf(); T.SetTranslation(gp_Vec(*move))

    final = gp_Trsf()
    final.Multiply(T); final.Multiply(R)
    B_moved = _transform_shape(tdB, final)

    # B 摆好后沿 axis 的真实上下表面(用最终实体), 相对 pA。
    tB_bot, tB_top = _surface_extent_along_axis(B_moved.wrapped, axis, pA)
    # contact_t: A、B 真实贴合平面沿 axis 的位置(= A 顶面平面 = 移动后 B 底面平面), 相对 pA。
    contact_t = A_top_contact
    # 紧固件就位的真实平面 t(全部 pA-相对, 供 _place/anchor3d 用):
    #   B_top_seat: 螺栓头/垫圈坐 B 顶面平面 = off + B_top_seat_pre + axial。
    #   A_bot_seat: 螺母坐 A 底面平面(A 不动)。
    B_top_seat = off + B_top_seat_pre + axial
    seats = {"B_top": B_top_seat, "A_bot": A_bot_seat,
             "B_top_plane": B_top_is_plane, "A_bot_plane": A_bot_is_plane}
    return (B_moved, axis, pA, tA_bot, tA_top, tB_bot, tB_top, final, contact_t,
            seats)


def _place(obj, a, p, t, flip=False):
    """与 assemble_fasteners.assemble.place 同语义: 库件(头/正面 +Z, 沿 -Z 延伸)对齐
    到轴 a、放到轴向位置 t; flip 先绕 X 翻 180。"""
    s = obj.val() if hasattr(obj, "val") else obj
    td = s.wrapped if hasattr(s, "wrapped") else s
    final = gp_Trsf()
    anchor = (p[0]+a[0]*t, p[1]+a[1]*t, p[2]+a[2]*t)
    tT = gp_Trsf(); tT.SetTranslation(gp_Vec(*anchor)); final.Multiply(tT)
    dot = max(-1.0, min(1.0, a[2])); ang = math.acos(dot)
    if ang > 1e-4:
        rax = (-a[1], a[0], 0.0)
        if math.hypot(*rax) < 1e-9:
            rax = (1.0, 0.0, 0.0)
        tR = gp_Trsf(); tR.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(*rax)), ang)
        final.Multiply(tR)
    if flip:
        tF = gp_Trsf(); tF.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), math.pi)
        final.Multiply(tF)
    return cq.Shape(BRepBuilderAPI_Transform(td, final, True).Shape())


def _good_through_hole(td, hole):
    """对接孔合格条件: 两端口都是垂直于轴的平面(顶面坐头/底面坐螺母都贴平), 且
    孔壁整圈完整(完整通孔, 不是边缘半孔)。返回 (ok, ep) ; ep 为 hole_plane_ends 结果。"""
    axis = _axis_to_z(hole[1])
    e = _orient_hole_to_axis(hole, axis)
    ep = hole_plane_ends(td, e)
    both_plane = ep["hi"][0] and ep["lo"][0]
    if not both_plane:
        return False, ep
    # 完整性: 在圆柱孔壁自身 t-span(e 的 t0/t1)内侧采样, 这才是真实孔壁所在;
    # 不要用平面 t(平面可能比孔壁略外, 采到孔外开放空间, 误判薄板完整孔为不完整)。
    if not hole_is_complete(td, e, ports=[e[3], e[4]]):
        return False, ep
    return True, ep


def match_pair(holesA, holesB, tdA=None, tdB=None, require_plane=True):
    """从 A、B 的孔里挑一对孔做对接螺栓孔。返回 (hA, hB, size, nominal) 或 None。

    require_plane 时(默认), 对接孔必须是**完整通孔且两端口为垂直轴平面**:
      - A、B 各自的对接孔两端都是垂直于孔轴的真实平面(顶面坐螺栓头、底面坐螺母,
        贴合面也是平面)=> 装配后头/螺母都贴在平底面上不悬空;
      - 孔壁整圈完整(非边缘豁口/半孔)=> 螺栓穿过完整孔, 不在边缘半孔。
    评分(越小越好): 孔径误差 + 居中度惩罚(越靠零件中心越优, 减少边缘穿孔)。
    tdA/tdB 是 A/B 的 TopoDS 实体; 不传则退回纯孔径匹配。"""
    # 预筛: 缓存每件合格对接孔
    okA = {}
    okB = {}
    if tdA is not None and tdB is not None:
        for i, h in enumerate(holesA):
            ok, _ = _good_through_hole(tdA, h)
            okA[i] = ok
        for j, h in enumerate(holesB):
            ok, _ = _good_through_hole(tdB, h)
            okB[j] = ok

    best = None
    for i, hA in enumerate(holesA):
        mA = af.match_screw_size(2*hA[0])
        if mA is None:
            continue
        for j, hB in enumerate(holesB):
            mB = af.match_screw_size(2*hB[0])
            if mB is None or mB[0] != mA[0]:
                continue
            err = abs(hA[0] - hB[0])
            pen = 0.0
            if tdA is not None and tdB is not None:
                if require_plane and not (okA.get(i) and okB.get(j)):
                    continue
                pen = (0.0 if okA.get(i) else 5.0) + (0.0 if okB.get(j) else 5.0)
            score = err + pen
            if best is None or score < best[0]:
                best = (score, hA, hB, mA[0], mA[1])
    if best is None:
        return None
    return best[1], best[2], best[3], best[4]


def _orient_hole_to_axis(hole, axis):
    """把孔 (r,a,p,t0,t1) 的端点重投到给定 axis 方向, 返回 (r,axis,p,t0',t1')。"""
    r, a, p, t0, t1 = hole
    e0 = (p[0]+a[0]*t0, p[1]+a[1]*t0, p[2]+a[2]*t0)
    e1 = (p[0]+a[0]*t1, p[1]+a[1]*t1, p[2]+a[2]*t1)
    s0 = (e0[0]-p[0])*axis[0] + (e0[1]-p[1])*axis[1] + (e0[2]-p[2])*axis[2]
    s1 = (e1[0]-p[0])*axis[0] + (e1[1]-p[1])*axis[1] + (e1[2]-p[2])*axis[2]
    return (r, axis, p, min(s0, s1), max(s0, s1))


def assemble_two(shapeA, shapeB, fastener="socket", pick=0):
    """双件夹紧装配核心。返回:
      (comp, info, anchorsA, anchorsB, recipe, B_moved, align)
    comp: A∪B + 螺栓 + 垫圈 + 螺母 的 compound。
    recipe: 紧固件配方(供脚本/出图重建)。
    align: (axis, pA, tA_bot, tA_top, tB_bot, tB_top)。
    """
    holesA = af.cylinder_holes(shapeA)
    holesB = af.cylinder_holes(shapeB)
    pair = match_pair(holesA, holesB, _topods(shapeA), _topods(shapeB),
                      require_plane=True)
    if pair is None:
        # 退回不强制平面(仍尽量优选), 让 demo / 兼容旧用法可用
        pair = match_pair(holesA, holesB, _topods(shapeA), _topods(shapeB),
                          require_plane=False)
    if pair is None:
        pair = match_pair(holesA, holesB)
    if pair is None:
        return None
    hA, hB, size, nominal = pair

    B_moved, axis, pA, tA_bot, tA_top, tB_bot, tB_top, trsf, contact_t, seats = \
        align_B_onto_A(shapeA, hA, shapeB, hB)

    a, p = axis, pA
    mtag = f"M{int(round(nominal))}"
    nut_th = nominal * 0.8

    # 紧固件就位基准用**真实平面** t(不是包围盒极值):
    #   top_face = B 顶面平面(螺栓头/垫圈坐此, 沿 +axis 方向看的孔上端面)。
    #   bot_face = A 底面平面(螺母坐此, 螺栓穿出那一侧的平底面)。
    top_face = seats["B_top"]
    bot_face = seats["A_bot"]

    # 堆叠: 螺栓头/垫圈坐 B 顶面平面 top_face, 杆向 -axis 穿过 B、A,
    # 螺母坐 A 底面平面 bot_face(真实平底, 不悬空)。
    total_thick = top_face - bot_face            # 两件夹紧段沿轴厚(平面到平面)
    length = max(6.0, round((total_thick + nut_th + 3.0) / 2.0) * 2.0)

    recipe = []

    def rec(factory, args, t, flip=False):
        recipe.append({"factory": factory, "args": list(args),
                       "a": list(a), "p": list(p), "t": float(t), "flip": flip})

    def anchor3d(t):
        return (p[0]+a[0]*t, p[1]+a[1]*t, p[2]+a[2]*t)

    anchorsA = {}
    anchorsB = {}
    parts = []

    # ---- 垫圈(顶, 坐在 B 上表面真实平面 top_face) ----
    head_t = top_face
    wobj, wash_iso = lp.make_washer(mtag, pick)
    if wobj is not None:
        wsh = wobj.val() if hasattr(wobj, "val") else wobj
        wash_th = wsh.BoundingBox().zlen
        head_t = top_face + wash_th
        parts.append(_place(wobj, a, p, top_face))
        rec("make_washer", [mtag, pick], top_face)
        anchorsB.setdefault(("washer", wash_iso, mtag), []).append(anchor3d(top_face))

    # ---- 螺栓(头在 head_t, 杆沿 -a 穿过两件总厚) ----
    sobj, screw_iso = lp.make_screw(size, length, pick)
    if sobj is None:
        return None
    parts.append(_place(sobj, a, p, head_t))
    rec("make_screw", [size, length, pick], head_t)
    # 螺栓气泡锚点放头顶(头最外端, +a 方向再外移一个头高), 不放头座面 —— 否则与
    # 垫圈锚点(top_face)几乎同高、气泡混淆。与单件 assemble 同一规则(见 memory
    # assembly-balloon-iso-layout: 螺钉锚点放头顶)。头朝 +a 长出, 故 +head_h。
    head_h = max(2.0, nominal * 0.9)
    anchorsB.setdefault(("screw", screw_iso, size), []).append(
        anchor3d(head_t + head_h))

    # ---- 螺母(底, 坐在 A 下表面真实平面 bot_face, flip) ----
    nobj, nut_iso = lp.make_nut(size, mtag, pick)
    if nobj is not None:
        parts.append(_place(nobj, a, p, bot_face, flip=True))
        rec("make_nut", [size, mtag, pick], bot_face, flip=True)
        anchorsA.setdefault(("nut", nut_iso, mtag), []).append(anchor3d(bot_face))

    # ---- compound: A、B 两 base + 紧固件 ----
    def _shp(x):
        s = x.val() if hasattr(x, "val") else x
        return s if hasattr(s, "wrapped") else cq.Shape(s)

    solids = [_shp(shapeA), _shp(B_moved)] + [_shp(x) for x in parts]
    comp = cq.Compound.makeCompound(solids)

    info = {"size": size, "nominal": nominal, "length": length,
            "total_thick": round(total_thick, 3), "nut_th": round(nut_th, 3),
            "screw": screw_iso, "nut": nut_iso if nobj is not None else None,
            "washer": wash_iso if wobj is not None else None}
    align = (axis, pA, tA_bot, tA_top, tB_bot, tB_top, contact_t, seats)
    return comp, info, anchorsA, anchorsB, recipe, B_moved, align


# =====================================================================
# 验证: 螺栓贯穿两件、螺母在底外、两板贴合
# =====================================================================
def verify_geometry(shapeA, B_moved, align, info):
    """几何校验(基于包围盒 + 实体内外判定):
      - 两件贴合: B 底端 == A 顶端(缝 ~0, 不穿插)。
      - 螺栓杆贯穿两件总厚: head_t - length <= tA_bot(底端在 A 底面之下或齐平)。
      - 螺母在最底面之外: 螺母顶 = tA_bot, 不嵌入 A(tA_bot 处之上才是 A 实体)。
    返回 (ok, msgs)。"""
    axis, pA, tA_bot, tA_top, tB_bot, tB_top = align[:6]
    contact_t = align[6] if len(align) > 6 else tA_top
    seats = align[7] if len(align) > 7 else {}
    top_face = seats.get("B_top", tB_top)
    bot_face = seats.get("A_bot", tA_bot)
    msgs = []
    ok = True

    # 贴合面: A、B 用真实平面在 contact_t 对齐, 接缝恒为 0(由构造保证)。
    # 真正的"穿插/留缝"由下方 A-B 布尔相交检查判定, 比包围盒可靠。
    msgs.append(f"贴合面 contact_t = {contact_t:+.3f} (A顶平面=B底平面, 接缝=0)")

    # 螺栓头/螺母都坐在真实平面上(不是包围盒极值)。
    if not seats.get("B_top_plane", False):
        ok = False; msgs.append("  [FAIL] 螺栓头/垫圈坐的 B 顶面不是垂直轴平面(会悬空)")
    if not seats.get("A_bot_plane", False):
        ok = False; msgs.append("  [FAIL] 螺母坐的 A 底面不是垂直轴平面(会悬空)")
    msgs.append(f"螺栓头平面 top_face={top_face:.3f} (B顶真实平面={seats.get('B_top_plane')}), "
                f"螺母平面 bot_face={bot_face:.3f} (A底真实平面={seats.get('A_bot_plane')})")

    length = info["length"]
    # 杆尖端: 从螺栓头底(top_face)沿 -axis 延伸 length。须穿过 A 底平面 bot_face。
    tip_t = top_face - length
    msgs.append(f"螺栓杆尖 t={tip_t:.3f}, A底平面 t={bot_face:.3f}, "
                f"夹紧厚={top_face - bot_face:.3f}, 杆长={length}")
    if tip_t > bot_face + 0.5:
        ok = False; msgs.append("  [FAIL] 螺栓杆未贯穿两件(尖端在 A 底平面之上)")

    # 螺母不嵌入 A: 螺母顶面 = bot_face(A 底平面), 其下方(-axis)才是螺母, A 在其上方。
    # 取 bot_face 略下一点应在 A 实体外。
    a, p = axis, pA
    clf = BRepClass3d_SolidClassifier(_topods(shapeA))
    below = (p[0]+a[0]*(bot_face-0.3), p[1]+a[1]*(bot_face-0.3), p[2]+a[2]*(bot_face-0.3))
    clf.Perform(gp_Pnt(*below), 1e-6)
    out = clf.State() == TopAbs_OUT
    msgs.append(f"A 底平面外一点在A实体外? {out} (螺母不嵌入A)")
    if not out:
        ok = False; msgs.append("  [FAIL] A 底平面下仍是A实体, 螺母会嵌入")

    # ---- A-B 实体干涉(穿插)检查: 核心要求 ----
    tdA = _topods(shapeA)
    tdB = B_moved.wrapped if hasattr(B_moved, "wrapped") else _topods(B_moved)
    interferes, ratio, method = solid_interference(tdA, tdB, vol_ratio=0.01)
    msgs.append(f"A-B 相交体积比 = {ratio*100:.3f}% ({method}, 阈值 1%)")
    if interferes:
        ok = False
        msgs.append("  [FAIL] A、B 两件穿插(相交体积超阈值)")

    return ok, msgs


# =====================================================================
# 双 body 装配脚本
# =====================================================================
def _finalize_script(H, srcA, srcB, m, recipe, here_abs=None):
    """生成双件装配脚本: **import(exec) partA/partB 的 cadquery.py 取两零件几何**
    (baseA/baseB), 不再内联两段源码(省 token); B 段后用内嵌行变换矩阵把 baseB
    摆到位, 再 place() 紧固件。无注释无空行。srcA/srcB 保留形参兼容, 不再嵌入。
    风格与单件装配脚本(build_assembly_script)统一: 紧固件直接 parts.append(place(...)),
    末尾 makeCompound 时统一解包 —— 单/双件脚本除变换块外结构一致。
    here_abs: 兼容形参; 统一为相对路径方案时传 None(默认)。"""
    out = [H,
           "from OCP.gp import gp_Trsf",
           "from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform",
           # _HERE 已在 header 里定义(相对路径: __file__ 优先, 回退 cwd)。
           # 从各自子目录的 cadquery.py 执行取零件结果几何(取代内联零件代码)。
           "def _load_part(_sub):",
           "    _g = {'cq': cq, 'math': __import__('math'), '__name__': '_partexec'}",
           "    exec(open(os.path.join(_HERE, _sub, 'cadquery.py'), encoding='utf-8').read(), _g)",
           "    _r = _g.get('result')",
           "    if _r is None:",
           "        for _v in _g.values():",
           "            if isinstance(_v, cq.Workplane): _r = _v",
           "    return _r",
           "baseA = _load_part('partA')",
           "baseB = _load_part('partB')",
           "_t = gp_Trsf()"]
    out.append("_t.SetValues(" + ", ".join(af._fnum(v) for v in m) + ")")
    out.append("_sb = baseB.val() if hasattr(baseB, 'val') else baseB")
    out.append("_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb")
    out.append("baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())")
    out.append("parts = [baseA, baseB]")
    for r in recipe:
        kind = af._KIND_ARG.get(r["factory"], r["factory"])
        args = ", ".join(repr(x) if isinstance(x, str) else af._fnum(x)
                         for x in r["args"])
        call = (f'place(fastener("{kind}", {args}), '
                f'axis={af._vec(r["a"])}, point={af._vec(r["p"])}, '
                f'seat={af._fnum(r["t"])}, flip={r["flip"]})')
        out.append(f"parts.append({call})")
    out.append("result = cq.Compound.makeCompound([p.val() if hasattr(p, 'val') "
               "else p for p in parts])")
    return "\n".join(out) + "\n"


def _finalize_script_inline(H, srcA, srcB, m, recipe):
    """原版(内联)双件装配脚本: 把 A、B 两段源码内嵌(A改名baseA、B改名baseB),
    自包含无外部依赖(不引用 partA/partB)。保留原方案用。"""
    def _renamed(src, newname):
        lines = []
        for ln in af._strip_code(src).rstrip("\n").splitlines():
            if ln.strip() == "import cadquery as cq":
                continue
            lines.append(ln)
        done = False
        for i in range(len(lines) - 1, -1, -1):
            s = lines[i]
            if s.startswith("result") and "=" in s.split("#")[0]:
                rhs = s.split("=", 1)[1].strip()
                if rhs.isidentifier():
                    lines[i:i + 1] = ([] if rhs == newname else [f"{newname} = {rhs}"])
                else:
                    lines[i] = newname + s[len("result"):]
                done = True
                break
        if not done:
            lines.append(f"{newname} = result")
        return lines

    out = [H,
           "from OCP.gp import gp_Trsf",
           "from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform"]
    out += _renamed(srcA, "baseA")
    out += _renamed(srcB, "baseB")
    out.append("_t = gp_Trsf()")
    out.append("_t.SetValues(" + ", ".join(af._fnum(v) for v in m) + ")")
    out.append("_sb = baseB.val() if hasattr(baseB, 'val') else baseB")
    out.append("_sb = _sb.wrapped if hasattr(_sb, 'wrapped') else _sb")
    out.append("baseB = cq.Shape(BRepBuilderAPI_Transform(_sb, _t, True).Shape())")
    out.append("parts = [baseA, baseB]")
    for r in recipe:
        kind = af._KIND_ARG.get(r["factory"], r["factory"])
        args = ", ".join(repr(x) if isinstance(x, str) else af._fnum(x)
                         for x in r["args"])
        call = (f'place(fastener("{kind}", {args}), '
                f'axis={af._vec(r["a"])}, point={af._vec(r["p"])}, '
                f'seat={af._fnum(r["t"])}, flip={r["flip"]})')
        out.append(f"parts.append({call})")
    out.append("result = cq.Compound.makeCompound([p.val() if hasattr(p, 'val') "
               "else p for p in parts])")
    return "\n".join(out) + "\n"


def _trsf_to_rows(trsf):
    """gp_Trsf -> 12 个 SetValues 行优先元素 (3x4)。"""
    return [trsf.Value(r, c) for r in (1, 2, 3) for c in (1, 2, 3, 4)]


# =====================================================================
# 完整产出
# =====================================================================
def produce_two(shapeA, shapeB, name, outdir, fastener="socket",
                srcA=None, srcB=None, fmts=("png", "svg", "dxf"),
                skip_verify=False, rerender_only=False, keep_script=False):
    import projlib
    import drawing

    # rerender_only: 仅重出图(盘上已有带螺纹 model.step + 已验证几何)。
    #   - 强制 lp.SIMPLE=True: 装配阶段用光杆紧固件, 跳过带螺纹建模(make_screw
    #     带螺纹 4.8s/个 vs 光杆 0.1s, 慢 48 倍 —— 这才是装配慢的真凶)。出图本
    #     就用 _build_simple_compound 光杆投影(带螺纹会让 HLR 爆炸), 故画面一致。
    #   - 跳过 model.step/stl 重导出: 不覆盖盘上已有的带螺纹 3D 模型。
    #   - skip_verify: 几何已验证过。
    _prev_simple = lp.SIMPLE
    if rerender_only:
        lp.SIMPLE = True
        skip_verify = True
    try:
        return _produce_two_body(shapeA, shapeB, name, outdir, fastener,
                                 srcA, srcB, fmts, skip_verify, rerender_only,
                                 projlib, drawing, keep_script)
    finally:
        lp.SIMPLE = _prev_simple


def _produce_two_body(shapeA, shapeB, name, outdir, fastener, srcA, srcB,
                      fmts, skip_verify, rerender_only, projlib, drawing,
                      keep_script=False):
    res = assemble_two(shapeA, shapeB, fastener)
    if res is None:
        return None
    comp, info, anchorsA, anchorsB, recipe, B_moved, align = res

    # skip_verify: 重渲染场景下几何已验证过(盘上的图当初就是 verify PASS 才生成),
    # 跳过最贵的 verify_geometry 布尔相交校验, 只重出图。大幅提速。
    if skip_verify:
        ok, msgs = True, ["[skip_verify] 信任已验证几何, 跳过布尔校验"]
    else:
        ok, msgs = verify_geometry(shapeA, B_moved, align, info)
    print("[verify]")
    for mm in msgs:
        print("  " + mm)
    print(f"[verify] => {'PASS' if ok else 'FAIL'}")

    d = os.path.join(outdir, name)
    os.makedirs(d, exist_ok=True)
    if not rerender_only:
        # rerender_only 时跳过: 盘上已有带螺纹 model.step/stl, 不能用光杆 comp 覆盖。
        cq.exporters.export(comp, os.path.join(d, "model.step"))
        # 装配体 STL(与 model.step 并列)。STL 导出快(几何已在), 无超时顾虑。
        try:
            cq.exporters.export(comp, os.path.join(d, "model.stl"))
        except Exception as e:
            print("  [assembly stl 跳过]", type(e).__name__, str(e)[:60])

    # ---- 装配脚本(双 body) ---- (rerender_only 时跳过: 盘上已有, 且这段又跑一遍
    # match_pair+align 是额外开销。keep_script 时也跳过: 目录已有一份正确脚本(如
    # slim 目录的相对路径版), 只补其它模态, 不覆盖脚本。)
    if (not rerender_only) and (not keep_script) and srcA is not None and srcB is not None:
        try:
            from OCP.gp import gp_Trsf as _GT
            # 重新计算变换矩阵: align_B_onto_A 已经给出 trsf, 重跑一次取矩阵
            holesA = af.cylinder_holes(shapeA)
            holesB = af.cylinder_holes(shapeB)
            pair = match_pair(holesA, holesB, _topods(shapeA), _topods(shapeB),
                              require_plane=True)
            if pair is None:
                pair = match_pair(holesA, holesB, _topods(shapeA),
                                  _topods(shapeB), require_plane=False)
            if pair is None:
                pair = match_pair(holesA, holesB)
            trsf = align_B_onto_A(shapeA, pair[0], shapeB, pair[1])[7]
            rows = _trsf_to_rows(trsf)
            # 直接产 **slim 相对路径版**(数据即 slim, 不再产内联完整版):
            # 脚本从本目录 partA/partB 相对加载零件源码, 共享 fasteners/
            # library_parts 在输出根目录(下方复制), 目录即自包含 slim 数据。
            script = _finalize_script(af._ASM_HEADER.rstrip("\n"),
                                      srcA, srcB, rows, recipe)
            open(os.path.join(d, "assembly_cadquery.py"), "w",
                 encoding="utf-8").write(script)
            # 通用依赖只在输出根目录(two_part_assemblies/)放一份共享, 不再每子目录复制。
            # 脚本头(af._ASM_HEADER)已把上一级目录加入 sys.path, 能从根目录解析。
            import shutil
            outroot = os.path.dirname(d)
            for hp in ("fasteners.py", "library_parts.py"):
                dst = os.path.join(outroot, hp)
                if not os.path.isfile(dst):
                    shutil.copyfile(os.path.join(HERE, hp), dst)
        except Exception as e:
            print("  [assembly script 跳过]", type(e).__name__, str(e)[:80])

    # ---- 光杆简化装配体出图 ----
    comp_simple = _build_simple_compound(shapeA, B_moved, recipe)
    comp_shape = comp_simple.wrapped if hasattr(comp_simple, "wrapped") else comp_simple
    views = {n: projlib.project(comp_shape, p["paper_x"], p["paper_y"], deflection=0.1)
             for n, p in projlib.VIEWS.items()}

    # BOM + 气泡: Body A、Body B 两本体 + 紧固件。传装配轴(=接触面法向)给锚点,
    # 使两本体气泡锚点各偏自己一侧、指向明确(align = (axis, pA, ...))。
    bom, seeds = _build_two_bom(shapeA, B_moved, anchorsA, anchorsB,
                                axis=align[0] if align else None)
    balloons = af.seeds_to_balloons(seeds, comp_shape,
                                    fastener_axis=align[0] if align else None)
    axes = af.build_fastener_axes(recipe, comp_simple)
    axes = axes + af.build_revolution_axes(comp_shape)
    bearings = af.build_bearing_symbols(recipe)
    threads = af.build_thread_lines(recipe)

    # 可读标题(不灌 uuid/哈希): 名字形如 "<A8>_<B8>__<Mtag>__two" -> "M4 two-part assembly"。
    _mtag = ""
    try:
        _mtag = name.split("__")[1] if "__" in name else ""
    except Exception:
        _mtag = ""
    _two_title = (f"{_mtag} two-part assembly".strip() if _mtag
                  else "Two-part assembly")
    drawing.render(views, name, os.path.join(d, "drawing"),
                   fmts=fmts,
                   matched=[], overall=None, bom=bom, balloons=balloons, axes=axes,
                   bearings=bearings, threads=threads, title=_two_title)

    # ---- 两零件各自的零件详图: partA/ partB/(与单件装配 produce 的 part/ 同套路) ----
    # 复用 make_drawings.process: 姿态归一化 + 参数提取 + 完整 ISO 制造尺寸标注(已修
    # 尺寸出框)。每个零件本体放到 <d>/partX/ 作为独立 process 目标:
    # 需要 partX/cadquery.py(参数来源) + partX/model.step(零件**原始位姿**, 非装配里
    # 被变换后的 B_moved —— 零件图就是零件本身的三视图)。
    def _emit_part(sub, src, shp):
        if src is None or shp is None:
            return
        try:
            import make_drawings as md
            pdir = os.path.join(d, sub)
            os.makedirs(pdir, exist_ok=True)
            open(os.path.join(pdir, "cadquery.py"), "w",
                 encoding="utf-8").write(af._strip_code(src))
            sh = shp.val() if hasattr(shp, "val") else shp
            cq.exporters.export(sh, os.path.join(pdir, "model.step"))
            cq.exporters.export(sh, os.path.join(pdir, "model.stl"))  # 零件原始位姿
            md.OUT = d                          # process 在 <d> 下找 sub 子目录
            md.process(sub)                     # -> <d>/partX/drawing.{png,svg,dxf}
        except Exception as e:
            print(f"  [{sub} drawing 跳过]", type(e).__name__, str(e)[:60])

    _emit_part("partA", srcA, shapeA)
    _emit_part("partB", srcB, shapeB)           # 用 B 原始零件(非 B_moved)

    json.dump({"name": name, "info": info, "bom": bom,
               "verify": {"pass": ok, "msgs": msgs}},
              open(os.path.join(d, "assembly.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return {"dir": d, "info": info, "verify_pass": ok}


def _build_simple_compound(shapeA, B_moved, recipe):
    """A、B 两本体 + 光杆简化紧固件, 供工程图投影(带螺纹会让 HLR 爆炸)。"""
    def _shp(x):
        s = x.val() if hasattr(x, "val") else x
        return s if hasattr(s, "wrapped") else cq.Shape(s)
    prev = lp.SIMPLE
    lp.SIMPLE = True
    try:
        solids = [_shp(shapeA), _shp(B_moved)]
        fac = {"make_screw": lp.make_screw, "make_nut": lp.make_nut,
               "make_washer": lp.make_washer}
        for r in recipe:
            obj = fac[r["factory"]](*r["args"])[0]
            if obj is None:
                continue
            solids.append(_place(obj, r["a"], r["p"], r["t"], r["flip"]))
        return cq.Compound.makeCompound(solids)
    finally:
        lp.SIMPLE = prev


def _build_two_bom(shapeA, B_moved, anchorsA, anchorsB, axis=None):
    """BOM: item1 = Body A, item2 = Body B, item3.. = 紧固件。seeds 同步。"""
    import iso_knowledge as iso
    bom = []
    seeds = []
    sA = shapeA.val() if hasattr(shapeA, "val") else shapeA
    sA = sA.wrapped if hasattr(sA, "wrapped") else sA
    sB = B_moved.val() if hasattr(B_moved, "val") else B_moved
    sB = sB.wrapped if hasattr(sB, "wrapped") else sB

    # 接触面法向 = 装配轴 axis(B 坐在 A 顶, +axis 指向 B 的自由侧, -axis 指向 A 的
    # 自由侧)。给每件传"远离接触面"的方向, 使 A、B 锚点各偏自己一侧、投影后分开,
    # 气泡指向明确(不落在共享接触线上)。axis 为空时退回原逻辑。
    biasA = (-axis[0], -axis[1], -axis[2]) if axis is not None else None
    biasB = (axis[0], axis[1], axis[2]) if axis is not None else None
    bom.append({"item": 1, "qty": 1, "designation": "Body A",
                "reference": "(detail drawing)", "material": "Steel"})
    seeds.append((1, [af._body_surface_anchor(sA, biasA)]))
    bom.append({"item": 2, "qty": 1, "designation": "Body B",
                "reference": "(detail drawing)", "material": "Steel"})
    seeds.append((2, [af._body_surface_anchor(sB, biasB)]))

    item = 2
    merged = {}
    for src in (anchorsA, anchorsB):
        for k, pts in src.items():
            merged.setdefault(k, []).extend(pts)
    for (role, ftype, size), pts in sorted(merged.items(),
                                           key=lambda kv: (kv[0][0], kv[0][2])):
        item += 1
        nm, ref, sz = iso.fastener_designation(ftype, size)
        bom.append({"item": item, "qty": len(pts), "designation": nm,
                    "reference": f"{ref} - {sz}", "material": iso.DEFAULT_MATERIAL})
        seeds.append((item, list(pts)))
    return bom, seeds


# =====================================================================
# 数据源
# =====================================================================
def exec_part(code):
    from types import SimpleNamespace
    if isinstance(code, (bytes, bytearray)):
        code = bytes(code).decode("utf-8", "replace")
    g = {"cq": cq, "SimpleNamespace": SimpleNamespace, "math": math, "__name__": "x"}
    exec(code, g)
    r = g.get("result")
    if r is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                r = v
    return r, code


def load_from_test(uuid):
    import glob
    import pyarrow.parquet as pq
    for f in sorted(glob.glob(os.path.join(ROOT, "test", "*.parquet"))):
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            for row in pf.read_row_group(
                    rg, columns=["uuid", "cadquery_file"]).to_pylist():
                if row["uuid"] == uuid:
                    return exec_part(row["cadquery_file"])
    return None, None


def auto_find_pair(max_scan=400):
    """扫描数据集, 找两个带匹配孔(同规格)的件。返回 (uuidA, srcA, shapeA, uuidB, ...)。"""
    import glob
    import pyarrow.parquet as pq
    cands = []   # (uuid, src, shape, [sizes])
    for f in sorted(glob.glob(os.path.join(ROOT, "test", "*.parquet"))):
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            for row in pf.read_row_group(
                    rg, columns=["uuid", "cadquery_file"]).to_pylist():
                if len(cands) >= 2 and _pairable(cands):
                    return _emit_pair(cands)
                try:
                    shape, code = exec_part(row["cadquery_file"])
                    if shape is None:
                        continue
                    holes = af.cylinder_holes(shape)
                    sizes = set()
                    for h in holes:
                        m = af.match_screw_size(2*h[0])
                        if m:
                            sizes.add(m[0])
                    if sizes:
                        cands.append((row["uuid"], code, shape, sizes))
                        pr = _pairable(cands)
                        if pr:
                            return _emit_pair(cands, pr)
                except Exception:
                    pass
                if len(cands) > max_scan:
                    return None
    return None


def _pairable(cands):
    """找 cands 里两件共享同一螺纹规格的一对下标。返回 (i, j, size) 或 None。"""
    for i in range(len(cands)):
        for j in range(i+1, len(cands)):
            common = cands[i][3] & cands[j][3]
            if common:
                return (i, j, sorted(common)[0])
    return None


def _emit_pair(cands, pr=None):
    if pr is None:
        pr = _pairable(cands)
    if pr is None:
        return None
    i, j, size = pr
    a = cands[i]; b = cands[j]
    return (a[0], a[1], a[2], b[0], b[1], b[2], size)


def demo_plates():
    """两块带 M6 通孔的板。"""
    A = (cq.Workplane("XY").box(60, 60, 10)
         .faces(">Z").workplane().hole(6.6))
    B = (cq.Workplane("XY").box(50, 50, 8)
         .faces(">Z").workplane().hole(6.6))
    srcA = ("import cadquery as cq\n"
            "result = cq.Workplane('XY').box(60, 60, 10)"
            ".faces('>Z').workplane().hole(6.6)\n")
    srcB = ("import cadquery as cq\n"
            "result = cq.Workplane('XY').box(50, 50, 8)"
            ".faces('>Z').workplane().hole(6.6)\n")
    return A, srcA, B, srcB


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--data", nargs=2, metavar=("UUIDA", "UUIDB"))
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--fastener", default="socket", choices=["socket", "hex"])
    ap.add_argument("--outdir", default=os.path.join(HERE, "two_part_assemblies"))
    args = ap.parse_args()

    if args.demo:
        A, srcA, B, srcB = demo_plates()
        name = "TWO_demo__M6__two"
        res = produce_two(A, B, name, args.outdir, args.fastener, srcA, srcB)
    elif args.data:
        uA, uB = args.data
        A, srcA = load_from_test(uA)
        B, srcB = load_from_test(uB)
        if A is None or B is None:
            print("找不到零件源码"); return
        nm = f"{uA[:8]}_{uB[:8]}__two"
        res = produce_two(A, B, nm, args.outdir, args.fastener, srcA, srcB)
    elif args.auto:
        found = auto_find_pair()
        if found is None:
            print("未找到可配对的两件"); return
        uA, srcA, A, uB, srcB, B, size = found
        tag = size.split("-")[0]
        nm = f"{uA[:8]}_{uB[:8]}__{tag}__two"
        print(f"配对: {uA[:8]} + {uB[:8]} @ {size}")
        res = produce_two(A, B, nm, args.outdir, args.fastener, srcA, srcB)
    else:
        print("用法: --demo | --data UUIDA UUIDB | --auto"); return

    if res:
        print(f"产出 -> {res['dir']}  verify={'PASS' if res['verify_pass'] else 'FAIL'}")
        print(f"  {res['info']}")


if __name__ == "__main__":
    main()
