"""自动检孔 -> 匹配规格螺钉 -> 拧入装配 -> 装配体几何(+三视图)。

任务书 "explore assembly data extension": 给真实毫米零件检测其圆柱孔, 按孔径
匹配 ISO 间隙配合的标准螺钉(可选垫圈/螺母), 沿孔轴对齐拧入, 得到装配体, 再走
现有工程图管线出三视图。输出隔离到 1m_Convert/assemblies/<uuid>/。

用法:
  python assemble_fasteners.py <step_or_uuid> [--fastener socket|hex|...] [--nut] [--washer]
  python assemble_fasteners.py --demo        # 用一个内置带孔零件演示
"""
import sys, os, math, argparse, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import cadquery as cq

# cq_warehouse 在 import 时会**全局替换** cadquery Shape 的 copy/fix/translate 等
# 方法为它自己的 BinTools 序列化版本; 该版本对某些几何会抛
# NCollection_IndexedMap::FindKey / BinTools ReadGeometry, 从而**连带搞坏原始零件
# 脚本里的 .shell()/.fix()**(它们内部调用 Shape.fix -> copy)。我们装配用的是
# 原生 OCP 变换(见 place), 不需要 cq_warehouse 的这些方法, 所以: 先备份 cadquery
# 原版方法, import 之后再恢复, 让原始零件脚本的 .shell() 等照常工作。
_S = cq.occ_impl.shapes.Shape
_CQ_ORIG = {n: getattr(_S, n) for n in
            ("copy", "fix", "translate", "rotate", "located", "moved",
             "_apply_transform") if hasattr(_S, n)}

from cq_warehouse.fastener import SocketHeadCapScrew, HexHeadScrew, HexNut, PlainWasher
import library_parts as lp

for _n, _f in _CQ_ORIG.items():           # 恢复 cadquery 原版方法
    try:
        setattr(_S, _n, _f)
    except Exception:
        pass

from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN, TopAbs_ON


def _is_internal_hole(solid, axis_pnt):
    """判定一个圆柱面是 内孔(可装螺栓) 还是 外圆(凸台/轴/圆盘外壁,不可装)。
    用实体内外判定, 与位姿/面取向无关, 最稳健: 取圆柱轴上、面跨度中点处的一点
    (axis_pnt). 内孔的轴心穿过空腔 => 该点在实体外; 实心轴/凸台的轴心是实体
    => 在实体内. 因此"轴心点在实体外"=> 内孔。返回 True=内孔。"""
    try:
        clf = BRepClass3d_SolidClassifier(solid)
        clf.Perform(gp_Pnt(axis_pnt[0], axis_pnt[1], axis_pnt[2]), 1e-6)
        st = clf.State()
        if st == TopAbs_IN or st == TopAbs_ON:
            return False                     # 轴心在实体内 => 实心圆柱(外圆), 不是孔
        return True                          # 轴心在实体外 => 内孔
    except Exception:
        return True

# ---- ISO 间隙配合: 孔的直径 -> 最接近的公制螺纹规格 (size, pitch) -----------
# 通孔(clearance)直径略大于螺纹公称径; 取 normal fit 表的近似阈值。
# 选规格的判据: 螺纹公称径 <= 孔径, 且孔径 - 公称径在合理间隙(<= ~1.2mm)内。
METRIC = [  # (公称径 mm, size 字符串, normal clearance 通孔直径 mm)
    (3.0,  "M3-0.5",  3.4),
    (4.0,  "M4-0.7",  4.5),
    (5.0,  "M5-0.8",  5.5),
    (6.0,  "M6-1",    6.6),
    (8.0,  "M8-1.25", 9.0),
    (10.0, "M10-1.5", 11.0),
    (12.0, "M12-1.75", 13.5),
]


def match_screw_size(hole_dia):
    """孔直径 -> 最合适的螺纹规格。优先选 clearance 通孔直径最接近孔径的规格;
    要求螺纹公称径 < 孔径(螺钉杆能穿过)。匹配不到返回 None。"""
    best = None
    for nominal, size, clr in METRIC:
        if nominal >= hole_dia + 0.05:
            continue                       # 杆比孔粗, 穿不过
        err = abs(clr - hole_dia)
        if err <= 1.6 and (best is None or err < best[0]):
            best = (err, size, nominal)
    return (best[1], best[2]) if best else None


def _to_topods(shape):
    """接受 Workplane / cq.Shape / TopoDS_Shape, 统一返回 TopoDS_Shape。"""
    if hasattr(shape, "val"):                 # Workplane
        shape = shape.val()
    if hasattr(shape, "wrapped"):             # cq.Shape
        return shape.wrapped
    return shape


def _perp_basis(a):
    """给轴向单位向量 a, 返回与之垂直的两个单位向量 (u, v) 构成正交基。"""
    ref = (0.0, 0.0, 1.0) if abs(a[2]) < 0.9 else (1.0, 0.0, 0.0)
    u = (a[1]*ref[2]-a[2]*ref[1], a[2]*ref[0]-a[0]*ref[2], a[0]*ref[1]-a[1]*ref[0])
    un = math.sqrt(u[0]*u[0]+u[1]*u[1]+u[2]*u[2]) or 1.0
    u = (u[0]/un, u[1]/un, u[2]/un)
    v = (a[1]*u[2]-a[2]*u[1], a[2]*u[0]-a[0]*u[2], a[0]*u[1]-a[1]*u[0])
    return u, v


def _radials8(a):
    """绕轴 a 圆周均布的 8 个单位径向向量。"""
    u, v = _perp_basis(a)
    out = []
    for k in range(8):
        ang = k * math.pi / 4.0
        c, s = math.cos(ang), math.sin(ang)
        out.append((u[0]*c+v[0]*s, u[1]*c+v[1]*s, u[2]*c+v[2]*s))
    return out


def _radials16(a):
    """绕轴 a 圆周均布的 16 个单位径向向量(整圆完整性判据用,比 8 向更密,
    能逮住更小的豁口/缺料弧段)。"""
    u, v = _perp_basis(a)
    out = []
    for k in range(16):
        ang = k * math.pi / 8.0
        c, s = math.cos(ang), math.sin(ang)
        out.append((u[0]*c+v[0]*s, u[1]*c+v[1]*s, u[2]*c+v[2]*s))
    return out


def _coaxial(a, p, b, q, ta=0.02, td=0.5):
    """两条轴 (a,p)/(b,q) 是否同轴(平行且共线): 方向近平行 且 轴上一点到对方轴的
    垂直距离 ~0。与 Location 漂移无关(只看方向 + 共线)。"""
    if abs(abs(a[0]*b[0]+a[1]*b[1]+a[2]*b[2]) - 1) >= ta:
        return False
    dp = (p[0]-q[0], p[1]-q[1], p[2]-q[2])
    cr = (dp[1]*a[2]-dp[2]*a[1], dp[2]*a[0]-dp[0]*a[2], dp[0]*a[1]-dp[1]*a[0])
    return math.sqrt(cr[0]*cr[0]+cr[1]*cr[1]+cr[2]*cr[2]) < td


def cylinder_holes(shape):
    """提取零件的**可装紧固件圆柱孔**: [(radius, axis_dir, axis_pnt, t0, t1)]。
    axis_dir 单位向量; t0/t1 沿轴的孔壁两端(相对锚定后的 axis_pnt)。

    稳健判据(与 OCCT Location 漂移无关 —— axis_pnt 重新锚定到 face 包围盒中心
    在轴线上的投影, 见下):
      C1 concave  : 圆柱面"料在半径外侧、孔内为空"(真孔/内腔壁都满足; 凸台/轴/
                    圆盘外圆等 convex 外圆不满足 -> 排除)。
      C2 无同轴薄壁外壁: 不存在 同轴(共线)的 convex 外壁圆柱面(半径更大)与之轴向
                    重叠 **且 环厚 <= K*r**(管壁相对孔径是薄壁)。空心管/壳的内腔壁
                    总有一个同轴外壁、环厚(=R-r)与孔径相当或更薄(outer.cut(inner));
                    而"在实心凸台中心钻的螺钉孔"虽也有同轴外圆(凸台外壁), 但环厚
                    R-r >> r(孔很小、料很厚) => 不算薄壁 -> 不排除。K=1.5。
      C3 端口可达 : 沿轴线从孔的两端口向外走, 把每个端口归类:
                    CLEAN  = 端口直接通向零件外部(干净开口);
                    BLIND  = 端口被实体堵住(盲孔底 / 开口在斜面或曲面上, 轴向看是料);
                    CAVITY = 端口先是空, 但沿轴向外走又撞回实体 => 开口通向**封闭
                             内腔**(破进空腔), 紧固件会悬在腔里。
                    只要有**任一端口 = CAVITY 即排除**; 否则(两端 CLEAN/BLIND 任意
                    组合, 含盲孔、斜面开口孔、侧壁破出的孔)都保留。
    """
    shape = _to_topods(shape)
    clf = BRepClass3d_SolidClassifier(shape)

    def _inside(pt):
        clf.Perform(gp_Pnt(pt[0], pt[1], pt[2]), 1e-7)
        st = clf.State()
        return st == TopAbs_IN or st == TopAbs_ON

    # 零件包围盒(端口可达测试用)
    sbb = Bnd_Box(); BRepBndLib.Add_s(shape, sbb)
    sx0, sy0, sz0, sx1, sy1, sz1 = sbb.Get()
    diag = math.sqrt((sx1-sx0)**2 + (sy1-sy0)**2 + (sz1-sz0)**2) or 1.0

    def _oob(pt):
        m = 0.5
        return (pt[0] < sx0-m or pt[0] > sx1+m or pt[1] < sy0-m or
                pt[1] > sy1+m or pt[2] < sz0-m or pt[2] > sz1+m)

    def _port_kind(start, d, step=0.6):
        """从端口 start 沿单位方向 d(轴向, 朝零件外) 步进, 归类该端口:
          'BLIND'  : start 本身在实体内 => 端口被料堵(盲孔底, 或开口在斜面/曲面上,
                     轴向看进去是料) —— 不是破腔, 真孔可以有这种端口。
          'CLEAN'  : start 在实体外, 一路走到包围盒外都没再撞实体 => 干净开口到外部。
          'CAVITY' : start 在实体外, 但沿轴向外走又**撞回实体** => 端口前面那段空是
                     **封闭内腔**, 孔破进腔里, 紧固件悬空 -> 该孔应排除。
        """
        if _inside(start):
            return 'BLIND'
        pt = start
        for _ in range(int(diag/step) + 5):
            pt = (pt[0]+d[0]*step, pt[1]+d[1]*step, pt[2]+d[2]*step)
            if _oob(pt):
                return 'CLEAN'
            if _inside(pt):
                return 'CAVITY'
        return 'CLEAN'

    # ---- 第一遍: 收集所有圆柱面的几何 + concavity ----
    cyls = []
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Cylinder:
            cyl = surf.Cylinder()
            r = cyl.Radius()
            ax = cyl.Axis().Direction()
            loc = cyl.Location()
            a = (ax.X(), ax.Y(), ax.Z())
            p = (loc.X(), loc.Y(), loc.Z())
            fb = Bnd_Box(); BRepBndLib.Add_s(face, fb)
            x0, y0, z0, x1, y1, z1 = fb.Get()
            # ---- 锚点修正: 用 face 包围盒中心 投影到轴线, 消除 Location 漂移 ----
            fc = (0.5*(x0+x1), 0.5*(y0+y1), 0.5*(z0+z1))
            tc = (fc[0]-p[0])*a[0] + (fc[1]-p[1])*a[1] + (fc[2]-p[2])*a[2]
            p = (p[0]+a[0]*tc, p[1]+a[1]*tc, p[2]+a[2]*tc)   # 锚定后的轴参考点
            ts = [(c[0]-p[0])*a[0] + (c[1]-p[1])*a[1] + (c[2]-p[2])*a[2]
                  for c in [(x0, y0, z0), (x1, y1, z1)]]
            t0, t1 = min(ts), max(ts)
            depth = t1 - t0
            # ---- C1 concave: 沿轴向 5 层 × 圆周 8 向, 比较 r+δ(外) vs r-δ(内)实体数 ----
            rads = _radials8(a)
            delta = max(0.4, 0.2*r)
            nax = 5
            oh = ih = 0
            for i in range(nax):
                tt = t0 + depth*(i+0.5)/nax
                cpt = (p[0]+a[0]*tt, p[1]+a[1]*tt, p[2]+a[2]*tt)
                ri = max(0.05, r-delta)
                for rd in rads:
                    if _inside((cpt[0]+rd[0]*(r+delta), cpt[1]+rd[1]*(r+delta),
                                cpt[2]+rd[2]*(r+delta))):
                        oh += 1
                    if _inside((cpt[0]+rd[0]*ri, cpt[1]+rd[1]*ri, cpt[2]+rd[2]*ri)):
                        ih += 1
            concave = oh > ih
            cyls.append(dict(r=r, a=a, p=p, t0=t0, t1=t1, concave=concave))
        exp.Next()

    def _axoverlap(f, g):
        """g 的轴向跨度(投到 f 的轴上)是否与 f 的 [t0,t1] 重叠。"""
        a, p = f["a"], f["p"]
        gs = []
        for tt in (g["t0"], g["t1"]):
            w = (g["p"][0]+g["a"][0]*tt, g["p"][1]+g["a"][1]*tt, g["p"][2]+g["a"][2]*tt)
            gs.append((w[0]-p[0])*a[0] + (w[1]-p[1])*a[1] + (w[2]-p[2])*a[2])
        g0, g1 = min(gs), max(gs)
        return not (g1 < f["t0"]-0.5 or g0 > f["t1"]+0.5)

    # ---- 第二遍: 用 C1/C2/C3 筛出真孔 ----
    holes = []
    for f in cyls:
        if not f["concave"]:
            continue                            # C1: convex 外圆, 不是孔
        a, p, r, t0, t1 = f["a"], f["p"], f["r"], f["t0"], f["t1"]
        # C2: 同轴**薄壁**外壁(空心管/壳内腔壁)。环厚 R-r <= K*r 才算薄壁内腔壁;
        # 实心凸台里钻的小螺钉孔虽也有同轴外圆(凸台外壁), 但 R-r >> r, 不触发。
        K_WALL = 1.5
        has_coax_outer = any(
            (g is not f) and (not g["concave"]) and (g["r"] > r + 0.5)
            and (g["r"] - r) <= K_WALL * r
            and _coaxial(a, p, g["a"], g["p"]) and _axoverlap(f, g)
            for g in cyls)
        if has_coax_outer:
            continue
        # C3: 端口归类 —— 任一端 CAVITY(破进封闭内腔)即排除; 盲孔/斜面孔保留。
        ea = (p[0]+a[0]*(t1+0.3), p[1]+a[1]*(t1+0.3), p[2]+a[2]*(t1+0.3))
        eb = (p[0]+a[0]*(t0-0.3), p[1]+a[1]*(t0-0.3), p[2]+a[2]*(t0-0.3))
        ka = _port_kind(ea, a)
        kb = _port_kind(eb, (-a[0], -a[1], -a[2]))
        if ka == 'CAVITY' or kb == 'CAVITY':
            continue                            # 端口通向封闭内腔, 不可装
        holes.append((r, a, p, t0, t1))
    # 合并**同轴(共线)**的圆柱孔面 —— 不论半径是否相同。一个沉头孔/cbore 由
    # 通孔(小径) + 沉头(大径)两段同轴圆柱面组成, 它们是**同一个物理孔**, 必须合成
    # 一个, 否则会被当成两个孔、在同一孔位塞两套不同规格的紧固件(严重干涉)。
    # 合并后: 半径取**最小**(通孔小径决定螺钉规格), 轴向跨度取两段的并集。
    merged = []
    for h in holes:
        r, a, p, t0, t1 = h
        hit = None
        for m in merged:
            # 同轴向(平行)
            if abs(abs(a[0]*m[1][0]+a[1]*m[1][1]+a[2]*m[1][2]) - 1) >= 0.02:
                continue
            # 共线: 轴上一点到对方轴的垂直距离 ~0(同一条轴线 => 同一个孔)
            dp = (p[0]-m[2][0], p[1]-m[2][1], p[2]-m[2][2])
            cross = (dp[1]*a[2]-dp[2]*a[1], dp[2]*a[0]-dp[0]*a[2], dp[0]*a[1]-dp[1]*a[0])
            if math.sqrt(sum(c*c for c in cross)) < 0.3:
                hit = m; break
        if hit:
            hit[0] = min(hit[0], r)             # 取最小半径(通孔决定螺钉规格)
            # 关键: 两段圆柱面的 t 各自相对自己的 axis 点 p, 不能直接 min/max。
            # 把本段的两个**世界端点**投到被合并段(hit)的 (a,p) 参考上再合并跨度。
            ha, hp = hit[1], hit[2]
            for tt in (t0, t1):
                wpt = (p[0]+a[0]*tt, p[1]+a[1]*tt, p[2]+a[2]*tt)   # 世界端点
                ht = (wpt[0]-hp[0])*ha[0] + (wpt[1]-hp[1])*ha[1] + (wpt[2]-hp[2])*ha[2]
                hit[3] = min(hit[3], ht); hit[4] = max(hit[4], ht)
        else:
            merged.append([r, a, p, t0, t1])

    # ---- C4 整圆完整性: 紧固件只装在**孔壁沿整个圆周(360°)闭合包裹**的整圆孔上,
    # 彻底排除 边缘半圆/豁口/孔壁缺一块(3/4 圆、半圆、缺一角)的不完整孔。
    #
    # 沿轴向密采若干层, 每层在圆周 16 方向(_radials16)测孔壁: 该方向上半径外侧
    # (r+δ)是否实体(料)、内侧(r-δ)是否空。该层 good = "外实内空"(有正常孔壁)的方
    # 向数。good >= 13/16 => 该层是 **CLOSED 整圈闭合层**(容许至多 3 个方向 ~67° 的
    # 缺口给 倒角/数值噪声)。阈值 13 由真实数据标定: 962 个候选孔的 best-layer good
    # 直方图在 12 处有明显空档(641 个孔 good=16, ~40 个 13~15 近完整, 其余密集落在
    # <=11 的"半圆/豁口"区), 取 13 既保住近完整孔、又卡掉用户示例的半圆(9/16)。
    #
    # 判据: 要求存在一段**实实在在的整圈闭合带**——最长连续 CLOSED 层的轴向长度
    # >= need(绝对值 ~0.8mm, 见下), 即孔至少有一处孔壁厚度的料把它整圈包住。
    #   - 边缘半圆/豁口/缺角孔: 缺料方位贯穿整个孔深, **每一层 good 都 < 13**(6/16、
    #     8/16、9/16、11/16 等), 一层 CLOSED 都没有 => 连续闭合带长 0 => 排除。
    #   - 正常整圆孔(含 沉头孔、入口带倒角/局部缺料的孔、穿凹槽/内腔的通孔): 至少在
    #     某段孔壁处整圈闭合 => 有 CLOSED 带 => 保留。端口倒角/沉头层(非闭合)、穿腔的
    #     OPEN 空段都不影响"存在一段闭合带"。
    # 用"最长连续 CLOSED 带的绝对长度"而非"占孔深比例", 既不误判端口/穿腔过渡层、
    # 又能逮住贯穿整孔深的真豁口(它根本没有任何闭合带)。
    def _full_circle(r, a, p, t0, t1):
        if r < 0.3:
            return False
        rads = _radials16(a)
        n = len(rads)
        delta = max(0.4, 0.18 * r)
        depth = t1 - t0
        ri = max(0.05, r - delta)
        ro = r + delta
        nax = max(7, min(12, int(depth / 1.2) + 1))   # 密采, 控制层数(单件性能)
        dz = depth / nax                               # 每层代表的轴向厚度
        closed = []
        for i in range(nax):
            tt = t0 + depth * (i + 0.5) / nax
            cpt = (p[0]+a[0]*tt, p[1]+a[1]*tt, p[2]+a[2]*tt)
            good = 0
            for rd in rads:
                if (_inside((cpt[0]+rd[0]*ro, cpt[1]+rd[1]*ro, cpt[2]+rd[2]*ro))
                        and not _inside((cpt[0]+rd[0]*ri, cpt[1]+rd[1]*ri,
                                         cpt[2]+rd[2]*ri))):
                    good += 1
            closed.append(good >= n - 3)               # 该层是否整圈闭合(>=13/16)
        # 最长连续 CLOSED 段(层数)
        run = best = 0
        for c in closed:
            run = run + 1 if c else 0
            best = max(best, run)
        core_len = best * dz                            # 最长连续闭合带的轴向长度
        # 判据: 需要存在一段**实实在在的整圈闭合带**(连续 CLOSED 层), 其轴向长度
        # >= need。need 取**绝对值**(约 0.8mm 或半层, 取较小, 兜住极薄板), 而**不**按
        # 孔深比例——否则 穿过内腔/凹槽的通孔(closed 带只在两端孔壁处、中间是 OPEN
        # 空段)会因连续闭合段达不到"孔深的某比例"被误杀。真豁口/半圆孔每层 good 都
        # < 13, 一层 CLOSED 都没有 => core_len=0 => 排除; 而任何真孔总有一段孔壁厚度
        # 的整圈闭合带 => 通过。
        need = min(0.8, 0.6 * depth)
        return core_len >= need

    return [m for m in merged if _full_circle(m[0], m[1], m[2], m[3], m[4])]


def make_screw(size, length, kind="socket"):
    cls = {"socket": SocketHeadCapScrew, "hex": HexHeadScrew}.get(kind, SocketHeadCapScrew)
    ftype = {"socket": "iso4762", "hex": "iso4014"}.get(kind, "iso4762")
    return cls(size=size, length=length, fastener_type=ftype, simple=True)


def _seg_seg_dist(p1, q1, p2, q2):
    """两条 3D 线段 (p1->q1) 与 (p2->q2) 的最短距离。标准 clamped 参数解
    (Ericson, Real-Time Collision Detection)。返回最近距离(mm)。"""
    def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
    def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
    d1 = sub(q1, p1); d2 = sub(q2, p2); rr = sub(p1, p2)
    aa = dot(d1, d1); ee = dot(d2, d2); ff = dot(d2, rr)
    EPS = 1e-9
    if aa <= EPS and ee <= EPS:
        dv = rr; return dot(dv, dv) ** 0.5
    if aa <= EPS:
        s = 0.0; t = max(0.0, min(1.0, ff/ee))
    else:
        c = dot(d1, rr)
        if ee <= EPS:
            t = 0.0; s = max(0.0, min(1.0, -c/aa))
        else:
            b = dot(d1, d2); den = aa*ee - b*b
            s = max(0.0, min(1.0, (b*ff - c*ee)/den)) if den > EPS else 0.0
            t = (b*s + ff)/ee
            if t < 0.0:
                t = 0.0; s = max(0.0, min(1.0, -c/aa))
            elif t > 1.0:
                t = 1.0; s = max(0.0, min(1.0, (b - c)/aa))
    c1 = (p1[0]+d1[0]*s, p1[1]+d1[1]*s, p1[2]+d1[2]*s)
    c2 = (p2[0]+d2[0]*t, p2[1]+d2[1]*t, p2[2]+d2[2]*t)
    dv = sub(c1, c2); return dot(dv, dv) ** 0.5


def assemble(shape, fastener="socket", add_washer=False, add_nut=False,
             max_holes=8):
    """对 shape 的每个匹配孔生成并对齐拧入一个螺钉(+可选垫圈/螺母)。
    返回 (assembly_compound, report_list)。"""
    holes = cylinder_holes(shape)
    parts = [shape]
    report = []
    used = 0
    # 已放置紧固件的"杆"线段(轴 a, 过点 p, 轴向区间 [lo,hi], 杆半径 shaft_r)。
    # 用于检测两根紧固件的杆是否在空间里相交/重叠(典型错误: 一个竖直孔 + 一个
    # 水平孔在零件中心相交, 两根螺栓的杆就会穿插在一起)。本体干涉检测(_disk_*)
    # 只查"紧固件 vs 本体", 查不出"紧固件 vs 紧固件", 故单列此表。
    placed_shafts = []                # [(a, p, lo, hi, shaft_r)]
    # 每类部件的安放锚点(模型坐标): {kind_key: [(x,y,z), ...]} 供件号气泡用。
    # kind_key 用 (role, ftype, size): role=part/screw/washer/nut。
    anchors = {}
    # 装配"配方": 每个紧固件一条, 记录用哪个 library_parts 工厂、什么参数造出、
    # 以及 place 的摆放参数(a,p,t,flip)。供 build_assembly_script 写成可重跑脚本。
    recipe = []

    def rec(factory, args, a, p, t, flip=False):
        recipe.append({"factory": factory, "args": list(args),
                       "a": list(a), "p": list(p), "t": float(t), "flip": flip})

    def anchor3d(a, p, t):
        return (p[0] + a[0]*t, p[1] + a[1]*t, p[2] + a[2]*t)

    def place(obj, a, p, t, flip=False):
        """把一个库件(默认 头/正面在+Z、沿-z延伸)对齐到孔轴 a、放到轴向位置 t。
        flip=True 先绕 X 翻转180度(螺母/穿出端朝向相反)。
        用 OCP 原生 gp_Trsf 变换, 绕开 cq_warehouse 重写的 translate/copy
        (后者用 BinTools 序列化, 对某些几何会抛 NCollection/BinTools 异常)。"""
        from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir, gp_Vec
        from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
        s = obj.val() if hasattr(obj, "val") else obj
        td = s.wrapped if hasattr(s, "wrapped") else s
        # final = T · R · F  (作用到点: 先 flip, 再对齐 +Z->a, 最后平移)
        final = gp_Trsf()
        anchor = (p[0] + a[0]*t, p[1] + a[1]*t, p[2] + a[2]*t)
        tT = gp_Trsf(); tT.SetTranslation(gp_Vec(*anchor))
        final.Multiply(tT)
        dot = max(-1.0, min(1.0, a[2]))
        ang = math.acos(dot)
        if ang > 1e-4:
            rax = (-a[1], a[0], 0.0)
            if math.hypot(*rax) < 1e-9:
                rax = (1.0, 0.0, 0.0)
            tR = gp_Trsf()
            tR.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(*rax)), ang)
            final.Multiply(tR)
        if flip:
            tF = gp_Trsf()
            tF.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), math.pi)
            final.Multiply(tF)
        moved = BRepBuilderAPI_Transform(td, final, True).Shape()
        return cq.Shape(moved)

    # 螺钉头/螺母就位用"孔的局部上下端"(下面每个孔单独算), 不用整个零件包围盒:
    # 高锥体/异形件上, 用包围盒会把螺钉拉伸贯穿整个零件、头跑到远端。
    def proj_t(pt, a, p):
        return (pt[0]-p[0])*a[0] + (pt[1]-p[1])*a[1] + (pt[2]-p[2])*a[2]

    # 沿孔轴找零件的"真实上下表面": 圆柱孔面常被倒角/cbore 截短(0.5mm 倒角会让
    # 孔壁两端各缩 0.5mm), 直接用孔壁端点会让螺钉头/螺母嵌进倒角或料里。从孔壁
    # 端点沿轴**向外**步进, 在实体内就继续走, 一旦走出实体就到了真实表面 —— 这就
    # 是孔真正开口的料顶/料底。只在孔附近局部找(步进有上限), 不会像包围盒那样
    # 把高锥体的螺钉拉到远端。
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier as _Clf
    from OCP.gp import gp_Pnt as _GP
    from OCP.TopAbs import TopAbs_OUT as _OUT
    _sb = (shape.val() if hasattr(shape, "val") else shape)
    _solid_for_seat = _sb.wrapped if hasattr(_sb, "wrapped") else _sb

    def _radials(a):
        """绕轴 a 均布的 8 个单位径向向量(在孔壁四周取探测点)。孔可能只有一侧有
        料(另一侧是缺口/凹槽), 所以多方向探测, 任一方向在料里就算还没到表面。"""
        u = (1.0, 0.0, 0.0) if abs(a[0]) < 0.9 else (0.0, 1.0, 0.0)
        e1 = (a[1]*u[2]-a[2]*u[1], a[2]*u[0]-a[0]*u[2], a[0]*u[1]-a[1]*u[0])
        n1 = math.hypot(*e1); e1 = (e1[0]/n1, e1[1]/n1, e1[2]/n1)
        e2 = (a[1]*e1[2]-a[2]*e1[1], a[2]*e1[0]-a[0]*e1[2], a[0]*e1[1]-a[1]*e1[0])
        out = []
        for k in range(8):
            th = k * math.pi / 4.0
            c, s = math.cos(th), math.sin(th)
            out.append((e1[0]*c+e2[0]*s, e1[1]*c+e2[1]*s, e1[2]*c+e2[2]*s))
        return out

    def _surface_t_outward(p, a, t_start, sign, max_ext, r_off):
        """找零件真实表面: 孔轴在空腔里(分类恒 OUT)不能在轴上探测。在孔壁四周
        8 个方向 × **多个半径**(r_off、+0.6、+1.4)处沿轴向外步进: 只要还有任一
        探测点在料里就继续, 全部走出实体才到真实表面。多半径是为了跟随倒角斜面
        一直走到真实外表面(单一小半径会在倒角根部就判出界, 让件嵌进倒角)。
        返回该表面处的 t。"""
        clf = _Clf(_solid_for_seat)
        rads = _radials(a)
        offs = []
        for extra in (0.0, 0.6, 1.4):
            rr = r_off + extra
            offs += [(p[0]+rd[0]*rr, p[1]+rd[1]*rr, p[2]+rd[2]*rr) for rd in rads]
        step = 0.2
        t = t_start
        n = int(max_ext / step) + 1
        last_in = t_start
        for _ in range(n):
            any_in = False
            for po in offs:
                pt = (po[0]+a[0]*t, po[1]+a[1]*t, po[2]+a[2]*t)
                clf.Perform(_GP(*pt), 1e-6)
                if clf.State() != _OUT:
                    any_in = True; break
            if not any_in:
                break               # 四周都走出实体 -> 真实表面在此附近
            last_in = t
            t += sign * step
        return last_in

    def _bounded_by_material(p, a, t, r):
        """孔在轴向位置 t 处是否被 **真实料** 包住 —— 用紧贴孔壁的小半径(r+0.1~+0.3)
        在 8 个方向探测, 看是否存在 **对向成对** 两侧都有料的方向对。
        - 紧贴孔壁: 避免探到旁边的本体(如锥形支架/凸台壁)而误判。
        - 对向成对: 孔被料环绕(料顶/料底)时, 多对正对方向两侧都有料; 而旁边的本体
          只单侧贴着孔壁(另一侧是空的孔口/缺口), 至多凑出 1 对(本体壁正对处的料 +
          孔另一侧偶然的残料) -> 用"**至少 2 对**正对两侧都有料"把它排除。
        这正是螺钉头需要坐落的"孔真正穿出的料面": 头要坐在环绕孔的料上, 不能浮在
        只有单侧邻接本体的空中端点。"""
        clf = _Clf(_solid_for_seat)
        rads = _radials(a)
        base_pt = (p[0]+a[0]*t, p[1]+a[1]*t, p[2]+a[2]*t)
        for rr in (r + 0.1, r + 0.2, r + 0.3):
            ins = []
            for rd in rads:
                pt = (base_pt[0]+rd[0]*rr, base_pt[1]+rd[1]*rr, base_pt[2]+rd[2]*rr)
                clf.Perform(_GP(*pt), 1e-6)
                ins.append(clf.State() != _OUT)
            # 8 方向按 45° 均布, k 与 k+4 正好对向; 至少 2 对正对两侧都有料 = 被环绕
            if sum(1 for k in range(4) if ins[k] and ins[k + 4]) >= 2:
                return True
        return False

    def _seat_face_t(p, a, t_marched, sign, r, max_pull):
        """把(向外 march 得到的)端点收敛到螺钉头真正能坐的料面。
        若 t_marched 处孔壁已被料环绕(对向成对有料) -> 端点本就在真实料面/倒角外面,
        直接采用(保留 march 跟随倒角到外表面的能力, 不回拉)。
        否则端点悬在空中(只单侧贴着旁边本体, 如锥形支架壁) -> 沿轴 **向内** 步进,
        找到第一处孔壁被料环绕的位置, 即孔真正穿出的料面。"""
        if _bounded_by_material(p, a, t_marched, r):
            return t_marched
        step = 0.2
        n = int(max_pull / step) + 1
        t = t_marched
        for _ in range(n):
            t -= sign * step       # 向内(与向外 march 相反方向)
            if _bounded_by_material(p, a, t, r):
                return t
        return t_marched           # 没找到环绕料面: 保持原值(不恶化)

    def _slice_open(p, a, t, r, rmax):
        """在轴向位置 t、绕轴 8 向探测孔壁第一处料的半径, 归类该切片:
        返回 (near, open_, nohit):
          near  = 孔壁落在 r 附近(<= r+0.4)的方向数 —— 通孔小径壁。
          open_ = 孔壁明显比 r 大(> r+0.4, 直到 rmax)的方向数 —— 沉头大孔(cbore/csk)
                  把孔径在该端口扩大了, 紧贴小径处无料、要走到更大半径才撞料。
          nohit = 到 rmax 都没撞料的方向数(该方向通向零件外, 不参与判别)。
        沉头段切片特征: open_ 多、near 少; 通孔小径段: near 多、open_=0。"""
        rds = _radials(a)
        base = (p[0]+a[0]*t, p[1]+a[1]*t, p[2]+a[2]*t)
        clf = _Clf(_solid_for_seat)
        near = open_ = nohit = 0
        for rd in rds:
            rr = r - 0.3; found = None
            while rr <= rmax:
                pt = (base[0]+rd[0]*rr, base[1]+rd[1]*rr, base[2]+rd[2]*rr)
                clf.Perform(_GP(*pt), 1e-6)
                if clf.State() != _OUT:
                    found = rr; break
                rr += 0.1
            if found is None:
                nohit += 1
            elif found <= r + 0.4:
                near += 1
            else:
                open_ += 1
        return near, open_, nohit

    def _cbore_end(p, a, r, t_face, t_other):
        """检测孔在 t_face 这一端是否有沉头孔(counterbore/countersink)。从料面 t_face
        沿轴**向内**(朝 t_other)步进, 每个切片只看**命中料的那些径向方向**(忽略指向
        零件外的 nohit —— 孔常在料边缘, 半数方向没料):
          open_frac = open_/(open_+near) —— 命中方向里"孔壁比小径大(>r+0.4)"的比例。
          沉头段: 孔径被扩大, 命中方向几乎全是 open(open_frac 高);
          通孔小径段: 孔壁就在 r, 命中方向全是 near(open_frac=0)。
        连续 open_frac 高(>=0.5)的轴向长度 = 沉头深度; 其后第一处 open_frac==0(且有
        命中) = 沉头底(螺钉头座面)。返回 (has_cbore, floor_t):
          has_cbore = 连续扩孔段 >= 1.5mm; floor_t = 沉头底轴向位置(无沉头为 None)。
        """
        sign = 1.0 if t_other > t_face else -1.0
        rmax = r + 2.5
        span = abs(t_other - t_face)
        max_scan = min(span * 0.6, r + 8.0)   # 沉头不会占半个孔以上
        step = 0.2
        n = int(max_scan / step) + 1
        t = t_face
        open_run = 0.0       # 当前连续扩孔段轴向长度
        cbore_len = 0.0      # 见过的最长连续扩孔段
        seen_cbore = False
        floor_t = None
        for _ in range(n):
            near, open_, nohit = _slice_open(p, a, t, r, rmax)
            hits = near + open_
            if hits == 0:
                # 无命中(切片在料外): 不计入, 但也不打断已开始的扩孔段判定
                t += sign * step
                continue
            ofrac = open_ / hits
            is_open = ofrac >= 0.5                        # 命中方向多数是扩孔
            is_full = (open_ == 0 and near >= 1)          # 命中方向全是小径壁
            if is_open:
                open_run += step
                cbore_len = max(cbore_len, open_run)
                if open_run >= 1.5:
                    seen_cbore = True
            else:
                open_run = 0.0
            if seen_cbore and is_full:
                floor_t = t           # 扩孔段结束、撞上小径满壁 = 沉头底
                break
            t += sign * step
        has = seen_cbore
        if has and floor_t is None:
            # 见到沉头但没撞到明确小径满壁(渐变/斜面): 用扩孔段长度估座面
            floor_t = t_face + sign * cbore_len
        return has, floor_t

    def _nut_has_clearance(p, a, nut_t, out_sign, nominal):
        """螺母净空检测: 螺母坐在料面 nut_t、本体沿 out_sign 方向(朝零件外)伸出
        nut_th 厚、外接圆半径 ~0.9*nominal。在该占据区(螺母外缘环 × 沿轴几层)采样,
        若相当比例点落在**本体料**内 => 螺母会嵌进本体(如回转锥体外扩壁紧贴孔的
        穿出口) => 无净空, 返回 False。平板通孔的螺母端是空旷的料面外 => 占据区在
        料外 => 全部点在外 => True, 照常装螺母。
        out_sign = 螺母相对轴 a 的伸出方向(+1=沿 +a, -1=沿 -a)。"""
        nut_th = max(2.0, nominal * 0.8)
        r_out = nominal * 0.9                      # 螺母外接圆半径(对边 ~1.8*nominal)
        rads = _radials(a)
        clf = _Clf(_solid_for_seat)
        inside = 0; total = 0
        # 沿轴 3 层(贴料面、中间、远端外缘), 每层 8 向 × 外半径环上采样
        for fr in (0.15, 0.5, 0.95):
            tt = nut_t + out_sign * nut_th * fr
            base = (p[0]+a[0]*tt, p[1]+a[1]*tt, p[2]+a[2]*tt)
            for rd in rads:
                for rr in (r_out * 0.75, r_out):    # 螺母中外缘两圈
                    pt = (base[0]+rd[0]*rr, base[1]+rd[1]*rr, base[2]+rd[2]*rr)
                    clf.Perform(_GP(*pt), 1e-6)
                    total += 1
                    if clf.State() != _OUT:
                        inside += 1
        # >20% 占据点在本体料内 => 螺母嵌进本体, 无净空
        return total == 0 or (inside / total) <= 0.20

    # ---- 几何干涉检测: 紧固件的头/垫圈/螺母 是否嵌入本体或侧向撞凸起 ----
    # 用密集点采样(快, 无布尔, 避开螺纹螺旋面布尔崩溃 + 性能): 对头/垫圈/螺母的
    # **整个圆盘占据体积**(沿轴 nut_th/head_h 几层 × 圆周 12 向 × 半径多圈, 直到外缘
    # r_out≈0.9*公称径), 测落在本体料内的比例。圆盘比孔大, 嵌入或侧撞凸起(rib/凸台/
    # 台阶)时大量采样点会落在料内; 螺钉杆穿过通孔只在孔壁占一点点 -> 比例低。
    # 比例 > 阈值 => 该孔整组回退不装。螺钉杆本身不测(它本就在孔里)。
    _clf_int = _Clf(_solid_for_seat)

    def _disk_interferes(p, a, seat_t, out_sign, r_out, thick):
        """头/垫圈/螺母圆盘(座面 seat_t, 沿 out_sign*a 伸出 thick, 外缘 r_out)是否
        嵌料/撞凸起。沿轴 3 层 × 圆周 12 向 × 半径 3 圈采样, 内料比例 > 0.15 => 干涉。"""
        rads = _radials(a)                          # 8 向已够; 用现成的
        if len(rads) < 12:
            # 加密到 12 向
            u, v = _perp_basis(a)
            rads = [(u[0]*math.cos(k*math.pi/6)+v[0]*math.sin(k*math.pi/6),
                     u[1]*math.cos(k*math.pi/6)+v[1]*math.sin(k*math.pi/6),
                     u[2]*math.cos(k*math.pi/6)+v[2]*math.sin(k*math.pi/6)) for k in range(12)]
        inside = total = 0
        for fr in (0.1, 0.5, 0.9):
            tt = seat_t + out_sign * thick * fr
            base = (p[0]+a[0]*tt, p[1]+a[1]*tt, p[2]+a[2]*tt)
            for rd in rads:
                for rr in (r_out*0.5, r_out*0.78, r_out):   # 圆盘内中外三圈
                    pt = (base[0]+rd[0]*rr, base[1]+rd[1]*rr, base[2]+rd[2]*rr)
                    _clf_int.Perform(_GP(*pt), 1e-6)
                    total += 1
                    if _clf_int.State() != _OUT:
                        inside += 1
        return total > 0 and (inside / total) > 0.15

    # ---- 座面支撑检测(防悬空): 头/垫圈/螺母的座面(贴零件那一侧的圆环面) ----
    # _disk_interferes 只逮"圆盘嵌进料内", 逮不到"圆盘探出零件边缘悬空"(座面下方
    # 无料支撑) —— 边缘孔(或孔旁边就是内腔)上垫圈/头一部分悬在零件外/腔上, 座面圆环
    # 落空。这里沿座面圆环(孔径外侧 .. 圆盘外缘)圆周多方向(12)采样, 检测座面**正下方**
    # (贴零件那侧, 沿 -out_sign 朝零件内一个微小偏移)是否有料支撑:
    #   - 每个方向沿圆环半径带(r_lo .. r_out)取若干圈; 该方向的座面要被料整圈托住,
    #     **任一圈半径下方无料 => 该方向悬空**(座面在那处探出了零件/腔上)。
    #   - 悬空方向比例 > over_frac(默认 0.20, 即 >=3/12=25% 即触发, 2/12=17% 仍放过)
    #     => 圆盘探出边缘悬空 => 该孔判不合格(整孔回退, 与嵌入检测同一回退逻辑)。
    # 注意: 通孔的座面圆环中心是孔(空), 但圆环本身(半径在孔径外、圆盘外径内)应整圈
    # 落在料上 —— 故采样**整条半径带都要有料**才算该方向被支撑。
    def _disk_overhangs(p, a, seat_t, out_sign, r_out, r_hole, over_frac=0.20):
        """座面圆环下方支撑检测。seat_t=座面(贴料面)轴向位置, out_sign*a=圆盘伸出
        (朝零件外)方向 => 座面贴零件一侧在 -out_sign 方向。圆环半径带 (r_hole 外侧 ..
        r_out)。圆周 12 向, 每向在座面贴料侧紧邻处测整条半径带是否都有料; 任一处无料
        即该向悬空。悬空方向比例 > over_frac => 探出边缘/腔上悬空, 返回 True。"""
        u, v = _perp_basis(a)
        rads = [(u[0]*math.cos(k*math.pi/6)+v[0]*math.sin(k*math.pi/6),
                 u[1]*math.cos(k*math.pi/6)+v[1]*math.sin(k*math.pi/6),
                 u[2]*math.cos(k*math.pi/6)+v[2]*math.sin(k*math.pi/6)) for k in range(12)]
        # 圆环采样半径带: 落在孔径外、圆盘外缘内(避开正好在孔壁的数值噪声)。
        r_lo = max(r_hole + 0.4, r_out * 0.6)
        if r_lo >= r_out - 0.05:                 # 圆盘几乎不比孔大(无环), 不判悬空
            return False
        ring_rs = (r_lo, 0.5 * (r_lo + r_out), r_out - 0.1)
        # 座面贴零件一侧紧邻处: 沿 -out_sign 朝零件内偏移一点点(避开座面正好在表面上
        # 的 ON 噪声), 两个深度任一在料内即算该(方向,半径)有料。
        depths = (0.2, 0.6)
        overhang = 0
        for rd in rads:
            # 该方向被支撑 = 半径带上**每一圈**都有料(整条座面圆环线压在料上);
            # 任一圈无料 => 座面在那处探出零件/腔 => 该方向悬空。
            dir_supported = True
            for rr in ring_rs:
                ring_has_mat = False
                for dep in depths:
                    tt = seat_t - out_sign * dep
                    base = (p[0]+a[0]*tt, p[1]+a[1]*tt, p[2]+a[2]*tt)
                    pt = (base[0]+rd[0]*rr, base[1]+rd[1]*rr, base[2]+rd[2]*rr)
                    _clf_int.Perform(_GP(*pt), 1e-6)
                    if _clf_int.State() != _OUT:
                        ring_has_mat = True; break
                if not ring_has_mat:
                    dir_supported = False; break
            if not dir_supported:
                overhang += 1
        return (overhang / len(rads)) > over_frac

    pick = 0   # 全局轮换下标: 让头型/螺母型/垫圈型/轴承型在不同孔上多样化
    for (r, a0, p, t0, t1) in sorted(holes, key=lambda h: -h[0]):
        if used >= max_holes:
            break
        # 暂存该孔起始处的 parts/recipe/report 长度, 干涉则回退到此
        _parts_n0, _recipe_n0, _report_n0 = len(parts), len(recipe), len(report)
        _anchor_snapshot = {k: len(v) for k, v in anchors.items()}
        dia = 2 * r
        # 孔的两个真实端点(原轴向 a0 上): 这是螺钉就位的"局部料厚", 不能用整个
        # 零件包围盒 —— 否则像高锥体那种, 螺钉会被拉伸贯穿整个零件、头跑到锥尖。
        end0 = (p[0]+a0[0]*t0, p[1]+a0[1]*t0, p[2]+a0[2]*t0)
        end1 = (p[0]+a0[0]*t1, p[1]+a0[1]*t1, p[2]+a0[2]*t1)
        # 轴向归一化为指向 +Z(世界向上): 库件天然 头/正面在上, 轴指上才不倒置。
        a = a0 if a0[2] >= 0 else (-a0[0], -a0[1], -a0[2])
        # 在(可能翻转后的)轴上, 用孔的两端定义 料底/料顶
        te0, te1 = proj_t(end0, a, p), proj_t(end1, a, p)
        bot_t, top_t = min(te0, te1), max(te0, te1)   # 孔壁的上下端(可能被倒角截短)
        # 通孔 vs 盲孔: 在孔壁下端**轴线上**再往下取一点(离开孔底一点点), 若它在
        # 实体内 => 孔底封死 = 盲孔(不能从底面穿出螺母); 在实体外 => 通孔。盲孔不
        # 装螺母(否则螺母会陷进孔底以下的实体里, 见 3fc549c9 那件)。
        below = (p[0]+a[0]*(bot_t-1.0), p[1]+a[1]*(bot_t-1.0), p[2]+a[2]*(bot_t-1.0))
        is_through = _is_internal_hole(_solid_for_seat, below)   # True=轴下点在料外=通孔
        # 把上下端从"孔壁端点"延伸到"零件真实表面": 倒角/cbore 会让孔壁两端各缩进
        # 一截, 直接坐孔壁端点会让螺钉头/螺母嵌进料里。向外步进找真实表面, 步进上限
        # 取局部小量(孔径+4mm), 保证只在孔附近找、不会拉到远端。
        max_ext = dia + 4.0
        r_off = r + 0.6                      # 探测点落在孔壁旁的实体里
        top_t = _surface_t_outward(p, a, top_t, +1, max_ext, r_off)
        # 料顶悬空回拉: 拔模/回转件上, 旁边的本体壁(如锥形支架)会单侧贴着孔壁一直
        # 延伸到孔壁端点以外, 让向外 march 误以为还在料里、把料顶停在空中端点 ->
        # 螺钉头浮在料面以上、与本体干涉(见 0cf1b265)。这里把料顶收敛到孔真正穿出、
        # 被料环绕的那个面(用紧贴孔壁的小半径 + 对向成对判据, 排除单侧邻接的本体)。
        # 向内回拉上限取孔壁全跨度: 端点最坏会被本体拖出整段孔壁那么远。
        top_t = _seat_face_t(p, a, top_t, +1, r, (top_t - bot_t) + max_ext)
        # 盲孔: 料底就用孔底(不向下 march, 否则会穿过孔底实体找到零件外底面)
        if is_through:
            bot_t = _surface_t_outward(p, a, bot_t, -1, max_ext, r_off)
        thick = top_t - bot_t

        # ----- 沉头孔(counterbore/countersink)检测: 哪端有沉头、沉头底(座面)在哪 -----
        # 沉头孔由"通孔小径 + 沉头大径"同轴两段组成; cylinder_holes 合并同轴段后丢了
        # "大孔在哪端"的信息。这里在两个真实料面端各独立探测孔径是否被扩大(_cbore_end),
        # 定位沉头端 + 座面 t。螺钉头要沉进沉头、座在沉头底, 不能浮在料面外、更不能装反。
        cb_bot, floor_bot = _cbore_end(p, a, r, bot_t, top_t)
        cb_top, floor_top = _cbore_end(p, a, r, top_t, bot_t)
        # 两端都判出沉头(罕见: 双面沉头)时, 取沉头更深的一端放头。普通通孔两端都 False。
        head_end = None      # None=无沉头(沿用原逻辑); 'bot'/'top'=沉头端(头沉这端)
        floor_t = None
        if cb_bot and cb_top:
            if (floor_bot - bot_t) >= (top_t - floor_top):
                head_end, floor_t = 'bot', floor_bot
            else:
                head_end, floor_t = 'top', floor_top
        elif cb_bot:
            head_end, floor_t = 'bot', floor_bot
        elif cb_top:
            head_end, floor_t = 'top', floor_top

        # ===== 按孔径分配库件 =====
        # 大孔: 轴承(外径≈孔径压入). 中孔: 热熔螺纹嵌件. 小孔: 螺钉套装。
        # (链轮/链需要贯穿轴或多盘中心距, 单板带孔零件无此结构, 故不强行套用。)
        placed_kind = None

        if dia >= lp.BEARING_MIN:
            bobj, iso_key, bsize = lp.make_bearing(dia, pick)
            if bobj is not None:
                z0b, z1b = lp.part_axial_extent(bobj)
                # 轴承宽度居中放进料厚(压入孔), 顶/底贴近料面
                seat = bot_t - z0b + max(0.0, (thick - (z1b - z0b)) / 2.0)
                parts.append(place(bobj, a, p, seat))
                rec("make_bearing", [dia, pick], a, p, seat)
                anchors.setdefault(("bearing", iso_key, bsize), []).append(
                    anchor3d(a, p, (bot_t + top_t) / 2.0))
                report.append({"hole_dia": round(dia, 2), "part": "bearing",
                               "iso": iso_key, "size": bsize})
                used += 1; pick += 1; placed_kind = "bearing"
            if placed_kind:
                continue

        if lp.HEATSET_RANGE[0] <= dia <= lp.HEATSET_RANGE[1]:
            hobj, iso_key, hsize = lp.make_heatset(dia)
            if hobj is not None:
                z0h, z1h = lp.part_axial_extent(hobj)
                # 嵌件从料顶压入(开口朝上), 顶面齐料顶
                parts.append(place(hobj, a, p, top_t - z1h))
                rec("make_heatset", [dia], a, p, top_t - z1h)
                anchors.setdefault(("insert", iso_key, hsize), []).append(
                    anchor3d(a, p, top_t))
                report.append({"hole_dia": round(dia, 2), "part": "heatset",
                               "iso": iso_key, "size": hsize})
                used += 1; pick += 1; placed_kind = "insert"
            if placed_kind:
                continue

        # ----- 小孔: 螺钉套装(头型/螺母/垫圈按 pick 轮换) -----
        m = match_screw_size(dia)
        if m is None:
            continue
        size, nominal = m
        mtag = f"M{int(round(nominal))}"
        nut_th = nominal * 0.8
        # 沉头孔的就位方向: 螺钉头沉进沉头端, 头座面=沉头底, 头朝沉头那一侧(料外),
        # 杆穿向另一端, 螺母在另一端料面外。普通通孔: 沿用原逻辑(头在 top_t 朝 +a,
        # 螺母在 bot_t)。库件本地: 头座面 z=0、头向 +z、杆向 -z; place 把 +z 对齐 +a,
        # flip=True 先翻 180 度让头朝 -a。
        # place 的几何约定下:
        #   头朝 +a(无 flip): 头座面坐在 seat, 头向 +a 长出, 杆向 -a。
        #   头朝 -a(flip)   : 头座面坐在 seat, 头向 -a 长出, 杆向 +a。
        if head_end == 'top':
            # 沉头在 +a 端(top): 头座面=top 侧沉头底, 头朝 +a(无 flip), 杆向 -a 穿过,
            # 螺母在 bot 端料面外(flip, 朝 -a 长出)。
            head_t = floor_t; head_flip = False
            nut_t = bot_t; nut_flip = True; nut_out_sign = -1.0
            span = head_t - bot_t
        elif head_end == 'bot':
            # 沉头在 -a 端(bot): 头座面=bot 侧沉头底, 头朝 -a(flip), 杆向 +a 穿过,
            # 螺母在 top 端料面外(无 flip, 朝 +a 长出)。
            head_t = floor_t; head_flip = True
            nut_t = top_t; nut_flip = False; nut_out_sign = +1.0
            span = top_t - head_t
        else:
            head_t = top_t; head_flip = False
            nut_t = bot_t; nut_flip = True; nut_out_sign = -1.0
            span = top_t - bot_t
        # 杆长: 通孔要从头座面跨过余下料厚 + 螺母 + 余量穿出对端; 盲孔只到孔深。
        if is_through:
            length = max(6.0, round((span + nut_th + 3.0) / 2.0) * 2.0)
        else:
            length = max(6.0, round(max(4.0, thick - 0.5) / 2.0) * 2.0)
        sobj, screw_iso = lp.make_screw(size, length, pick)
        if sobj is None:
            continue
        entry = {"hole_dia": round(dia, 2), "screw_size": size,
                 "fastener": screw_iso, "length": length, "parts": ["screw"]}
        # 垫圈: 普通孔放头下(头被垫圈抬高 wash_th); 沉头孔头沉在孔里, 不放头下垫圈
        # (会顶出沉头), 改放螺母侧。
        if add_washer and head_end is None:
            wobj, wash_iso = lp.make_washer(mtag, pick)
            if wobj is not None:
                wsh = (wobj.val() if hasattr(wobj, "val") else wobj)
                wash_th = wsh.BoundingBox().zlen
                head_t = top_t + wash_th
                parts.append(place(wobj, a, p, top_t))
                rec("make_washer", [mtag, pick], a, p, top_t)
                entry["parts"].append("washer")
                anchors.setdefault(("washer", wash_iso, mtag), []).append(
                    anchor3d(a, p, top_t))
        parts.append(place(sobj, a, p, head_t, flip=head_flip))
        rec("make_screw", [size, length, pick], a, p, head_t, flip=head_flip)
        # 螺钉气泡锚点放在**头顶**(头最外端), 不放头座面 —— 头座面与垫圈座面(top_t)
        # 几乎同高, 气泡会和垫圈混淆。把锚点沿头朝向再外移一个头高, 落在头顶, 一眼
        # 是螺钉头、不会和它下面的垫圈搞混(用户: 螺栓要靠近上面那一侧指出)。
        head_h = max(2.0, nominal * 0.9)               # 螺钉头高近似
        head_anchor_t = head_t + (head_h if not head_flip else -head_h)
        anchors.setdefault(("screw", screw_iso, size), []).append(
            anchor3d(a, p, head_anchor_t))
        # 螺母只在**通孔**装(从对端料面穿出); 盲孔不装螺母(否则陷进孔底实体里)。
        # 再加净空检测: 螺母端被本体料包围(如回转锥体外扩壁紧贴孔的穿出口)时不装
        # 螺母——螺钉头沉 cbore、杆拧进孔即可(很多沉头螺钉就是拧螺纹孔不用螺母)。
        if add_nut and is_through and _nut_has_clearance(p, a, nut_t, nut_out_sign, nominal):
            nobj, nut_iso = lp.make_nut(size, mtag, pick)
            if nobj is not None:
                parts.append(place(nobj, a, p, nut_t, flip=nut_flip))
                rec("make_nut", [size, mtag, pick], a, p, nut_t, flip=nut_flip)
                entry["parts"].append("nut")
                anchors.setdefault(("nut", nut_iso, mtag), []).append(
                    anchor3d(a, p, nut_t))
        # ---- 干涉检测: 该孔的紧固件(头/垫圈/螺母/螺钉)是否嵌入本体或撞凸起 ----
        # 检查 头/垫圈 圆盘(座面 head_t, 沿头朝向伸出)与 螺母 圆盘(座面 nut_t, 沿
        # nut_out_sign 伸出)是否嵌料/撞凸起。头朝向: head_flip=True 朝 -a, 否则 +a。
        head_out = -1.0 if head_flip else 1.0
        head_disk_r = nominal * 1.15               # 头(含垫圈)外缘半径
        head_disk_th = max(2.0, nominal * 0.9)     # 头+垫圈厚
        nut_disk_r = nominal * 0.95
        nut_disk_th = max(2.0, nominal * 0.8)
        _has_nut = entry["parts"].count("nut") > 0
        # 沉头孔(head_end != None)的头**本来就沉在 cbore 凹腔里**, 周围是 cbore 壁的料,
        # 不对它做干涉检测(否则把正常沉头误判撞料)。只检测突出料面外的普通头。
        _interf = False
        if head_end is None:
            _interf = _disk_interferes(p, a, head_t, head_out, head_disk_r, head_disk_th)
        if (not _interf) and _has_nut:
            _interf = _disk_interferes(p, a, nut_t, nut_out_sign, nut_disk_r, nut_disk_th)
        # ---- 座面支撑检测(防悬空): 头/垫圈/螺母座面圆环下方是否有料 ----
        # _disk_interferes 只逮"嵌料", 逮不到"座面探出零件边缘/内腔悬空"(座面下方无料)。
        # 突出料面外的头/垫圈座面=top_t(垫圈/头座在料顶), 测其圆环下方支撑。沉头孔
        # (head_end != None)的头沉在 cbore 凹腔里、座在 cbore 底、周围是 cbore 壁料, 不做
        # 悬空检测(与 _disk_interferes 同样跳过, 否则把正常沉头误判)。螺母座面=nut_t(料
        # 面外)始终测。悬空方向 > 阈值 => 该孔整组回退不装(与嵌入同一回退逻辑)。
        if (not _interf) and head_end is None:
            _interf = _disk_overhangs(p, a, top_t, head_out, head_disk_r, r)
        if (not _interf) and _has_nut:
            _interf = _disk_overhangs(p, a, nut_t, nut_out_sign, nut_disk_r, r)
        # ---- 紧固件 vs 紧固件 干涉: 本根杆与已放置的杆是否在空间相交/重叠 ----
        # 两个互相垂直的孔(竖直孔 + 水平孔)会在零件中心相交, 两根螺栓的杆就穿插在
        # 一起(典型错误)。把本根杆当线段, 与每根已放置杆求最短距离; 小于两杆半径之和
        # (留一点间隙)即判为相交 -> 回退本孔(不装这根), 保留先放的(孔按孔径从大到小,
        # 先放的更"主"). 杆半径用公称径的一半 + 小余量。
        if not _interf:
            shaft_r = nominal * 0.5 + 0.3
            lo3 = (p[0]+a[0]*bot_t, p[1]+a[1]*bot_t, p[2]+a[2]*bot_t)
            hi3 = (p[0]+a[0]*top_t, p[1]+a[1]*top_t, p[2]+a[2]*top_t)
            for (sa, sp, slo, shi, sr) in placed_shafts:
                q0 = (sp[0]+sa[0]*slo, sp[1]+sa[1]*slo, sp[2]+sa[2]*slo)
                q1 = (sp[0]+sa[0]*shi, sp[1]+sa[1]*shi, sp[2]+sa[2]*shi)
                if _seg_seg_dist(lo3, hi3, q0, q1) < (shaft_r + sr - 0.2):
                    _interf = True
                    break
        if _interf:
            del parts[_parts_n0:]                # 删本孔新加的紧固件(本体在更前)
            del recipe[_recipe_n0:]
            del report[_report_n0:]
            for k in list(anchors.keys()):
                n0 = _anchor_snapshot.get(k, 0)
                if len(anchors[k]) > n0:
                    del anchors[k][n0:]
                if not anchors[k]:
                    del anchors[k]
            continue                             # 不计 used/pick, 跳过该孔
        # 通过全部检测: 登记本根杆, 供后续孔做杆-杆相交检测。
        placed_shafts.append((a, p, bot_t, top_t, nominal * 0.5 + 0.3))
        used += 1; pick += 1
        report.append(entry)
    # 组成 compound: 装配体里零件各自独立共存(不布尔熔合)。统一成 cq.Shape。
    solids = []
    for pp in parts:
        s = pp.val() if hasattr(pp, "val") else pp
        solids.append(s if hasattr(s, "wrapped") else cq.Shape(s))
    comp = cq.Compound.makeCompound(solids)
    return comp, report, anchors, recipe


def _body_surface_anchor(bb, bias_dir=None):
    """本体气泡锚点: 取一个真正落在本体实体表面上的点(不是包围盒角点, 那对
    L形/圆形/异形会落在空处). 做法: 从质心沿 -Z 找到本体顶面附近的一个真实
    顶点(取所有顶点里 z 最大、且在 XY 上离质心适中的一个), 保证点在实体上。

    bias_dir: 双件装配时传入"远离接触面"的单位方向(该 body 应指向的自己一侧)。
    给定时, 锚点改为优先选沿 bias_dir 最远的顶点 —— 这样 A、B 两件的锚点各自
    偏到自己远离接触面的一侧, 投影后两点分开, 气泡不再落在共享接触线上、指向明确。"""
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_VERTEX
    from OCP.TopoDS import TopoDS
    from OCP.BRep import BRep_Tool
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    pr = GProp_GProps(); BRepGProp.VolumeProperties_s(bb, pr)
    com = pr.CentreOfMass(); cx, cy = com.X(), com.Y()
    best = None  # (score, (x,y,z)); 偏好顶面、离质心有一定水平偏移的真实角点
    exp = TopExp_Explorer(bb, TopAbs_VERTEX)
    seen = set()
    while exp.More():
        p = BRep_Tool.Pnt_s(TopoDS.Vertex_s(exp.Current()))
        key = (round(p.X(), 3), round(p.Y(), 3), round(p.Z(), 3))
        if key not in seen:
            seen.add(key)
            off = math.hypot(p.X() - cx, p.Y() - cy)
            if bias_dir is not None:
                # 双件: 主导项 = 沿"远离接触面"方向的投影(选自己那一侧最外的顶点),
                # 使 A、B 锚点分居接触面两侧、投影后明显分开。离心作次要项破平手。
                proj = (p.X() * bias_dir[0] + p.Y() * bias_dir[1]
                        + p.Z() * bias_dir[2])
                score = proj * 3.0 + off * 0.5
            else:
                score = p.Z() * 2.0 + off      # 顶面优先, 兼顾离心避免和中心件重合
            if best is None or score > best[0]:
                best = (score, (p.X(), p.Y(), p.Z()))
        exp.Next()
    if best is not None:
        return best[1]
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    box = Bnd_Box(); BRepBndLib.Add_s(bb, box)
    x0, y0, z0, x1, y1, z1 = box.Get()
    return (x0, y0, z1)


def _readable_asm_title(uuid):
    """Human-readable assembly title for the ISO 7200 title block, from the dir
    name "<uuid>__<Mtag>_<fastener>__asm" -> e.g. "M4 socket assembly".
    Falls back to a generic "Assembly" if the name does not parse. NEVER returns
    the raw uuid/hash (user: the title must be readable, not an internal id)."""
    try:
        base = uuid[:-len("__asm")] if uuid.endswith("__asm") else uuid
        tail = base.split("__")[-1]              # "<Mtag>_<fastener>"
        if "_" in tail:
            mtag, fastener = tail.split("_", 1)
        else:
            mtag, fastener = tail, ""
        mtag = mtag.strip()
        fastener = fastener.replace("_", " ").strip()
        parts = [p for p in (mtag, fastener, "assembly") if p]
        title = " ".join(parts)
        return title if title.strip() else "Assembly"
    except Exception:
        return "Assembly"


def build_bom_and_balloons(part_shape, anchors, part_name="Body",
                           part_material="Steel"):
    """把装配 anchors 聚合成 ISO BOM + 件号气泡数据。
    件号: 1 = 非标零件本体(单独出零件图); 2.. = 各标准件(只进 BOM, 不画零件图)。
    返回 (bom_list, seeds) 其中 seeds=[(item, [inst3d, ...])]: 每个件号带它所有
    实例的真实 3D 锚点列表; 由布局求解器在三视图里择优 + 防重叠地放气泡。"""
    import iso_knowledge as iso
    bom = []
    seeds = []
    bb = (part_shape.val() if hasattr(part_shape, "val") else part_shape)
    bb = bb.wrapped if hasattr(bb, "wrapped") else bb
    item = 1
    bom.append({"item": 1, "qty": 1, "designation": part_name,
                "reference": "(detail drawing)", "material": part_material})
    seeds.append((1, [_body_surface_anchor(bb)]))     # 本体: 实体表面真实点
    for (role, ftype, size), pts in sorted(anchors.items(),
                                           key=lambda kv: (kv[0][0], kv[0][2])):
        item += 1
        name, ref, sz = iso.fastener_designation(ftype, size)
        bom.append({"item": item, "qty": len(pts), "designation": name,
                    "reference": f"{ref} - {sz}", "material": iso.DEFAULT_MATERIAL})
        seeds.append((item, list(pts)))                # 该件号的全部实例锚点
    return bom, seeds


def build_fastener_axes(recipe, comp_simple):
    """为每个紧固件/轴承生成 ISO 128 点画线中心线(沿其回转轴)。返回 render 用的
    axes=[{"view","x0","y0","x1","y1"}](各视图模型局部坐标)。中心线沿轴穿过紧固件、
    两端各伸出一截; 轴平行于视线的视图里中心线退化为点, 跳过。"""
    import projlib
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    views = ("front", "top", "left")
    # 装配体整体尺度, 决定中心线伸出长度
    cs = comp_simple.wrapped if hasattr(comp_simple, "wrapped") else comp_simple
    bx = Bnd_Box(); BRepBndLib.Add_s(cs, bx)
    x0, y0, z0, x1, y1, z1 = bx.Get()
    diag = math.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
    out = []
    # 去重同轴线(同 a、同 p 共线的紧固件只画一条中心线)
    seen = []
    for r in recipe:
        a = tuple(r["a"]); p = tuple(r["p"])
        # 该紧固件沿轴的覆盖范围(用 seat t 附近 + 余量); 简单用整体对角线的一半做半长
        key = None
        for s in seen:
            sa, sp = s
            if abs(abs(a[0]*sa[0]+a[1]*sa[1]+a[2]*sa[2]) - 1) < 0.02:
                dp = (p[0]-sp[0], p[1]-sp[1], p[2]-sp[2])
                cr = (dp[1]*a[2]-dp[2]*a[1], dp[2]*a[0]-dp[0]*a[2], dp[0]*a[1]-dp[1]*a[0])
                if math.sqrt(sum(c*c for c in cr)) < 0.3:
                    key = s; break
        if key is not None:
            continue
        seen.append((a, p))
        # 中心线长度 = 装配体沿该轴的真实跨度 + 小伸出(ISO 128: 中心线超出轮廓
        # 一小段即可, 不能用整体对角线那样冲出图框)。把 8 个包围盒角投到轴上取范围。
        corners = [(x0,y0,z0),(x1,y0,z0),(x0,y1,z0),(x1,y1,z0),
                   (x0,y0,z1),(x1,y0,z1),(x0,y1,z1),(x1,y1,z1)]
        ts = [(c[0]-p[0])*a[0]+(c[1]-p[1])*a[1]+(c[2]-p[2])*a[2] for c in corners]
        over = max(3.0, diag*0.04)          # 伸出量(~3mm 或 4% 对角线)
        tlo, thi = min(ts)-over, max(ts)+over
        e0 = (p[0]+a[0]*tlo, p[1]+a[1]*tlo, p[2]+a[2]*tlo)
        e1 = (p[0]+a[0]*thi, p[1]+a[1]*thi, p[2]+a[2]*thi)
        for v in views:
            px, py = projlib.VIEWS[v]["paper_x"], projlib.VIEWS[v]["paper_y"]
            dv = (px[1]*py[2]-px[2]*py[1], px[2]*py[0]-px[0]*py[2],
                  px[0]*py[1]-px[1]*py[0])     # 视线方向 = px × py
            if abs(a[0]*dv[0]+a[1]*dv[1]+a[2]*dv[2]) > 0.98:
                continue                        # 轴平行视线 -> 中心线退化为点, 跳过
            ax0 = e0[0]*px[0]+e0[1]*px[1]+e0[2]*px[2]
            ay0 = e0[0]*py[0]+e0[1]*py[1]+e0[2]*py[2]
            ax1 = e1[0]*px[0]+e1[1]*px[1]+e1[2]*px[2]
            ay1 = e1[0]*py[0]+e1[1]*py[1]+e1[2]*py[2]
            out.append({"view": v, "x0": ax0, "y0": ay0, "x1": ax1, "y1": ay1})
    return out


def build_bearing_symbols(recipe):
    """ISO 8826-1 简化轴承符号数据。对每个 make_bearing 配方, 算其世界中心 =
    place(a,p,t) 后的中心(库件本地居中, 故中心 = p + a*t), 投影到三视图:
      端视图(轴≈视线方向): end_on=True, 给出 OD/bore 圆 + 中心十字所需的 cx,cy。
      侧视图(轴在纸面内): end_on=False, 给出矩形(OD×width)中心 + 投影后的轴方向。
    返回 render() 用的 bearings=[{view, cx, cy, od, bore, width, end_on, ax, ay}]。"""
    import projlib
    import library_parts as _lp
    views = ("front", "top", "left")
    out = []
    for r in recipe:
        if r["factory"] != "make_bearing":
            continue
        res = _lp.make_bearing(*r["args"])      # (obj, iso_key, size串)
        if res[2] is None:
            continue
        bore, od, w = _lp.bearing_dims(res[2])
        a = tuple(r["a"]); p = tuple(r["p"]); t = float(r["t"])
        center = (p[0] + a[0]*t, p[1] + a[1]*t, p[2] + a[2]*t)
        for v in views:
            px, py = projlib.VIEWS[v]["paper_x"], projlib.VIEWS[v]["paper_y"]
            dv = (px[1]*py[2]-px[2]*py[1], px[2]*py[0]-px[0]*py[2],
                  px[0]*py[1]-px[1]*py[0])         # 视线方向 = px × py
            cx = center[0]*px[0] + center[1]*px[1] + center[2]*px[2]
            cy = center[0]*py[0] + center[1]*py[1] + center[2]*py[2]
            end_on = abs(a[0]*dv[0]+a[1]*dv[1]+a[2]*dv[2]) > 0.98
            # 轴在纸面内的投影方向(侧视图矩形朝向)
            axp = a[0]*px[0] + a[1]*px[1] + a[2]*px[2]
            ayp = a[0]*py[0] + a[1]*py[1] + a[2]*py[2]
            out.append({"view": v, "cx": cx, "cy": cy, "od": od, "bore": bore,
                        "width": w, "end_on": end_on, "ax": axp, "ay": ayp})
    return out


def build_thread_lines(recipe):
    """ISO 6410 外螺纹约定画法数据(螺钉杆)。对每个 make_screw 配方, 杆沿 -a 方向
    从 head_t 起、长度 length 延伸; 大径 = 螺纹公称径(M5->5)。小径取 0.85×大径。
    侧/正视图(轴在纸面内): 沿杆身两侧各加一条小径细实线(代表小径轮廓)。
    端视图(轴≈视线方向): 杆端面加一段 3/4 圈小径细线圆弧。
    返回 render() 用的 threads=[{view, x0,y0,x1,y1} 或 {view, end_on, cx, cy, r}]。"""
    import projlib
    import re as _re
    views = ("front", "top", "left")
    out = []
    for r in recipe:
        if r["factory"] != "make_screw":
            continue
        size = r["args"][0]; length = float(r["args"][1])
        m = _re.match(r"M([0-9.]+)", str(size))
        if not m:
            continue
        major = float(m.group(1))
        minor = 0.85 * major
        a = tuple(r["a"]); p = tuple(r["p"]); head_t = float(r["t"])
        # 杆方向: 默认头朝 +a、杆沿 -a; flip=True(沉头孔头沉在 -a 端)时头朝 -a、杆沿 +a。
        sd = +1.0 if r.get("flip") else -1.0   # 杆延伸方向(相对 a)
        # 杆轴线: head 端在 +a*head_t, 杆沿 sd*a 延伸 length。螺纹覆盖整个杆长。
        head = (p[0] + a[0]*head_t, p[1] + a[1]*head_t, p[2] + a[2]*head_t)
        tip = (head[0] + sd*a[0]*length, head[1] + sd*a[1]*length, head[2] + sd*a[2]*length)
        # 杆身留一点(头下方一点起画小径线), 端面留一点
        for v in views:
            px, py = projlib.VIEWS[v]["paper_x"], projlib.VIEWS[v]["paper_y"]
            dv = (px[1]*py[2]-px[2]*py[1], px[2]*py[0]-px[0]*py[2],
                  px[0]*py[1]-px[1]*py[0])
            end_on = abs(a[0]*dv[0]+a[1]*dv[1]+a[2]*dv[2]) > 0.98
            if end_on:
                cx = head[0]*px[0] + head[1]*px[1] + head[2]*px[2]
                cy = head[0]*py[0] + head[1]*py[1] + head[2]*py[2]
                out.append({"view": v, "end_on": True, "cx": cx, "cy": cy,
                            "r": minor / 2.0})
                continue
            # 轴在纸面内: 投影 head/tip, 沿轴的垂直方向偏移 ±minor/2 画两条小径线
            hx = head[0]*px[0] + head[1]*px[1] + head[2]*px[2]
            hy = head[0]*py[0] + head[1]*py[1] + head[2]*py[2]
            tx = tip[0]*px[0] + tip[1]*px[1] + tip[2]*px[2]
            ty = tip[0]*py[0] + tip[1]*py[1] + tip[2]*py[2]
            dx, dy = tx - hx, ty - hy
            ln = math.hypot(dx, dy)
            if ln < 1e-6:
                continue                            # 轴≈视线已被 end_on 捕获
            ux, uy = dx / ln, dy / ln
            nx, ny = -uy, ux                         # 垂直轴的单位向量
            off = minor / 2.0
            # 头下方一点起、端面收一点, 让小径线落在裸杆段内
            hx2, hy2 = hx + ux*0.5, hy + uy*0.5
            tx2, ty2 = tx - ux*0.5, ty - uy*0.5
            for s in (+1, -1):
                ox, oy = nx*off*s, ny*off*s
                out.append({"view": v, "x0": hx2+ox, "y0": hy2+oy,
                            "x1": tx2+ox, "y1": ty2+oy})
    return out


def build_revolution_axes(comp_shape):
    """任务3: 给装配投影体(光杆简化, 含本体)里所有回转体的圆加 ISO 128 中心线。
    用 projlib.circles_for_views 取各视图里显示为真圆的特征(本体孔/圆台/轴承圆等),
    给每个圆画一个十字中心线(短点画线, 长度≈直径+小伸出)。返回 axes=[{view,...}],
    与 build_fastener_axes 的输出格式一致, 由 render 合并为点画线。"""
    import projlib
    out = []
    try:
        circ = projlib.circles_for_views(comp_shape)
    except Exception:
        return out
    # 过滤伪圆: 真回转特征(孔/圆台/轴)半径有限; 弯曲件的大圆弧外轮廓会被
    # circles_for_views 误当成大"圆"(rad 几十 mm), 给它画中心线就成了横穿全图的
    # 长线(见 1ef536ac 香蕉件 TOP 视图 ~100mm 中心线)。半径 > 上限的不画中心线。
    RAD_MAX = 25.0          # 真孔/圆台半径上限(超过视为大圆弧轮廓, 非回转特征)
    EXT_CAP = 15.0          # 中心十字半长上限(只作标记, 不横穿全图)
    # ISO 128 / ISO 129-1: 中心线只画在**去除材料的完整圆特征**上——圆孔/沉孔/
    # 凸台口(diameter 目标, 用 ⌀ 标注)、完整回转体。圆角(fillet)/倒圆(round)是
    # "不去除材料的弧", 按 ISO 用半径 R 标注、**不画中心线**; 部分弧/边缘缺口同理。
    # projlib.circles_for_views 已按此语义给出字段: is_hole=孔/凸台口(去除材料),
    # is_full=完整 360° 圆; 圆角被显式标为 is_hole=False, is_full=False。故判据:
    #   画中心线  <=>  is_hole OR is_full   (直接对应 ISO"去除材料的完整圆")
    for v, lst in circ.items():
        seen = []
        for (rad, cx, cy, is_full, is_hole, cov) in lst:
            if rad > RAD_MAX:
                continue                            # 大圆弧轮廓, 非回转特征
            if not (is_hole or is_full):
                continue                            # 圆角/部分弧: 按 ISO 不画中心线
            # 去重: 同位置同半径只画一次
            if any(abs(cx-sx) < 0.3 and abs(cy-sy) < 0.3 and abs(rad-sr) < 0.1
                   for (sx, sy, sr) in seen):
                continue
            seen.append((cx, cy, rad))
            ext = min(rad + min(2.5, rad * 0.25), EXT_CAP)   # 十字半长(直径+小伸出, 封顶)
            out.append({"view": v, "x0": cx - ext, "y0": cy,
                        "x1": cx + ext, "y1": cy})
            out.append({"view": v, "x0": cx, "y0": cy - ext,
                        "x1": cx, "y1": cy + ext})
    return out


def seeds_to_balloons(seeds, shape, view=None, fastener_axis=None, fastener_item_min=3):
    """把每个件号的全部实例 3D 锚点投影到三视图坐标, 交给布局求解器。
    返回 render() 用的 balloons=[{"item", "insts":[{"view","x","y"}...]}]:
    每个件号给出它在 front/top/left 各自的候选投影点, 求解器据此择优避让。

    fastener_axis: 装配轴(紧固件堆叠方向)。给定时, 对紧固件件号
    (item >= fastener_item_min, 即 body 之后的 螺母/螺钉/垫圈 等) 跳过"轴垂直于
    纸面"的视图: 沿轴俯视时, 同轴的 螺母/垫圈/螺钉 会投影到同一点, 三个气泡挤在一起
    分不清是哪个零件; 而在轴平行于纸面的侧视图(FRONT/LEFT)里它们沿轴分开, 各自清晰。
    因此紧固件只在能把它们分开的视图里出候选。"""
    import projlib
    views = ("front", "top", "left")
    ax = None
    if fastener_axis is not None:
        import math as _m
        n = _m.sqrt(sum(c * c for c in fastener_axis)) or 1.0
        ax = tuple(c / n for c in fastener_axis)
    out = []
    for (item, insts) in seeds:
        cand = []
        is_fastener = ax is not None and item >= fastener_item_min
        for (x, y, z) in insts:
            for v in views:
                px, py = projlib.VIEWS[v]["paper_x"], projlib.VIEWS[v]["paper_y"]
                # A fastener stack collapses in a view whose paper plane is perpendicular
                # to the assembly axis, i.e. the axis projects to ~0 on BOTH paper axes.
                if is_fastener:
                    axp = abs(sum(ax[i] * px[i] for i in range(3)))
                    ayp = abs(sum(ax[i] * py[i] for i in range(3)))
                    if axp < 0.1 and ayp < 0.1:
                        continue        # skip the axis-aligned (collapsing) view
                vx = x*px[0] + y*px[1] + z*px[2]
                vy = x*py[0] + y*py[1] + z*py[2]
                cand.append({"view": v, "x": vx, "y": vy})
        out.append({"item": item, "insts": cand})
    return out


# 装配脚本前导段: fasteners/library_parts 两个通用 helper 不再复制进每个装配目录,
# 而是共享放在输出根目录(assemblies/ 或 two_part_assemblies/, 即本脚本的上一级)。
# 脚本把上一级目录加入 sys.path, 再 `from fasteners import` 即可解析。
_ASM_HEADER = '''import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.insert(0, os.path.dirname(_HERE))
import cadquery as cq
from fasteners import fastener, place
'''


def _asm_header(here_abs=None):
    """装配脚本头。here_abs 给定时把绝对目录硬编码为 _HERE(在 import fasteners 前生效),
    这样 CQ-editor 等无 __file__、cwd 不对的环境也能直接跑; 目录不存在(脚本被移动)则
    回退 __file__/cwd。fasteners 在其上一级, 故 sys.path 加 dirname(_HERE)。"""
    if not here_abs:
        return _ASM_HEADER.rstrip("\n")
    return (
        "import os, sys\n"
        "_HERE = r%r\n" % here_abs +
        "if not os.path.isdir(_HERE):\n"
        "    _HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()\n"
        "sys.path.insert(0, os.path.dirname(_HERE))\n"
        "import cadquery as cq\n"
        "from fasteners import fastener, place"
    )

# 每类紧固件的可读注释名
_KIND_LABEL = {
    "make_screw": "screw", "make_nut": "nut", "make_washer": "washer",
    "make_bearing": "bearing", "make_heatset": "heat-set insert",
}
# recipe.factory -> fasteners.fastener 的 kind 名
_KIND_ARG = {
    "make_screw": "screw", "make_nut": "nut", "make_washer": "washer",
    "make_bearing": "bearing", "make_heatset": "heatset",
}


def _recipe_compound(part_shape, recipe, simple):
    """按 recipe 重建装配 compound, 指定紧固件是否带螺纹(simple=True 光杆)。
    出图投影用 simple=True 的轻量体, 避开带螺纹螺旋面的 HLR 爆炸。"""
    import library_parts as _lp
    from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir, gp_Vec
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
    fac = {"make_screw": _lp.make_screw, "make_nut": _lp.make_nut,
           "make_washer": _lp.make_washer, "make_bearing": _lp.make_bearing,
           "make_heatset": _lp.make_heatset}

    def _place(obj, a, p, t, flip):
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

    prev = _lp.SIMPLE
    _lp.SIMPLE = simple
    try:
        bb = (part_shape.val() if hasattr(part_shape, "val") else part_shape)
        bb = bb if hasattr(bb, "wrapped") else cq.Shape(bb)
        solids = [bb]
        for r in recipe:
            # 出图(simple)时轴承几何**完全去掉**: 改由 ISO 8826-1 约定符号(矩形+十字 /
            # 圆+十字, 见 build_bearing_symbols + drawing._build_bearings)在 drawing 层
            # 直接用线条表达, 不再投影任何轴承实体。三维(非 simple)仍用真实轴承。
            if simple and r["factory"] == "make_bearing":
                continue
            else:
                obj = fac[r["factory"]](*r["args"])[0]
            if obj is None:
                continue
            solids.append(_place(obj, r["a"], r["p"], r["t"], r["flip"]))
        return cq.Compound.makeCompound(solids)
    finally:
        _lp.SIMPLE = prev


def _strip_code(src):
    """去掉源码里的整行注释和空行(行内 # 注释保留, 避免误删字符串里的 #)。
    零件脚本与装配脚本统一用此风格(用户要求: 不要注释和空行)。"""
    if isinstance(src, (bytes, bytearray)):
        src = bytes(src).decode("utf-8", "replace")
    out = []
    for ln in src.splitlines():
        st = ln.strip()
        if not st or st.startswith("#"):
            continue
        out.append(ln)
    return "\n".join(out) + "\n"


def _fnum(x):
    """把浮点写成简洁形式: 整数去小数, 否则 3 位有效。"""
    xr = round(float(x), 3)
    if abs(xr - round(xr)) < 1e-6:
        return str(int(round(xr)))
    return repr(xr)


def _vec(v):
    return "(" + ", ".join(_fnum(c) for c in v) + ")"


def build_assembly_script(body_src, recipe, here_abs=None):
    """生成装配脚本: **exec 子目录 part/cadquery.py 取主体零件几何**(base), 不再内联
    主体源码(省 token), 再用 fastener()/place() 把每个紧固件装上去, 最后
    result = 完整装配体。无注释、无空行。body_src 保留形参兼容, 不再嵌入。
    here_abs: 该脚本所在目录绝对路径, 硬编码进脚本 -> CQ-editor 等无 __file__ 环境
    也能直接定位 part/(不必 chdir); 目录不存在时回退 __file__/cwd。"""
    lines = [_asm_header(here_abs)]
    # 从 part/cadquery.py 执行取主体零件结果几何(取代内联零件源码)。
    # _HERE 已在 header 里定义(硬编码绝对路径优先, 移位后回退 __file__/cwd)。
    lines += [
        "def _load_part(_sub):",
        "    _g = {'cq': cq, 'math': __import__('math'), '__name__': '_partexec'}",
        "    exec(open(os.path.join(_HERE, _sub, 'cadquery.py'), encoding='utf-8').read(), _g)",
        "    _r = _g.get('result')",
        "    if _r is None:",
        "        for _v in _g.values():",
        "            if isinstance(_v, cq.Workplane): _r = _v",
        "    return _r",
        "base = _load_part('part')",
    ]
    lines.append("parts = [base]")
    for r in recipe:
        kind = _KIND_ARG.get(r["factory"], r["factory"])
        args = ", ".join(repr(x) if isinstance(x, str) else _fnum(x)
                         for x in r["args"])
        call = (f'place(fastener("{kind}", {args}), '
                f'axis={_vec(r["a"])}, point={_vec(r["p"])}, '
                f'seat={_fnum(r["t"])}, flip={r["flip"]})')
        lines.append(f"parts.append({call})")
    lines.append("result = cq.Compound.makeCompound([p.val() if hasattr(p, 'val') "
                 "else p for p in parts])")
    return "\n".join(lines) + "\n"


def build_assembly_script_inline(body_src, recipe):
    """原版(内联)单件装配脚本: 内嵌主体零件源码(产物改名 base), 自包含无外部依赖
    (不引用 part/)。保留原方案用。"""
    body_lines = []
    for ln in _strip_code(body_src).rstrip("\n").splitlines():
        if ln.strip() == "import cadquery as cq":
            continue
        body_lines.append(ln)
    renamed = False
    for i in range(len(body_lines) - 1, -1, -1):
        s = body_lines[i]
        if s.startswith("result") and "=" in s.split("#")[0]:
            rhs = s.split("=", 1)[1].strip()
            if rhs.isidentifier():
                body_lines[i:i + 1] = ([] if rhs == "base" else [f"base = {rhs}"])
            else:
                body_lines[i] = "base" + s[len("result"):]
            renamed = True
            break
    if not renamed:
        body_lines.append("base = result")
    lines = [_ASM_HEADER.rstrip("\n")]
    lines.extend(body_lines)
    lines.append("parts = [base]")
    for r in recipe:
        kind = _KIND_ARG.get(r["factory"], r["factory"])
        args = ", ".join(repr(x) if isinstance(x, str) else _fnum(x)
                         for x in r["args"])
        call = (f'place(fastener("{kind}", {args}), '
                f'axis={_vec(r["a"])}, point={_vec(r["p"])}, '
                f'seat={_fnum(r["t"])}, flip={r["flip"]})')
        lines.append(f"parts.append({call})")
    lines.append("result = cq.Compound.makeCompound([p.val() if hasattr(p, 'val') "
                 "else p for p in parts])")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="model.step 路径 或 output/koor uuid")
    ap.add_argument("--fastener", default="socket", choices=["socket", "hex"])
    ap.add_argument("--washer", action="store_true")
    ap.add_argument("--nut", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--outdir", default=os.path.join(HERE, "assemblies"))
    args = ap.parse_args()

    if args.demo:
        # 内置: 一块带 4 个 M6 通孔的板
        plate = (cq.Workplane("XY").box(80, 50, 10)
                 .faces(">Z").workplane()
                 .pushPoints([(-25, -12), (25, -12), (-25, 12), (25, 12)])
                 .hole(6.6))
        shape = plate
        uuid = "demo_plate"
    else:
        t = args.target
        if t and t.endswith(".step"):
            from OCP.STEPControl import STEPControl_Reader
            from OCP.IFSelect import IFSelect_RetDone
            rd = STEPControl_Reader(); rd.ReadFile(t); rd.TransferRoots()
            shape = cq.Workplane(obj=cq.Shape(rd.OneShape()))
            uuid = os.path.splitext(os.path.basename(t))[0]
        else:
            import make_drawings as md
            for base in (os.path.join(ROOT, "output"),
                         os.path.join(HERE, "koor_geometry")):
                sp = os.path.join(base, t, "model.step")
                if os.path.isfile(sp):
                    shape = cq.Workplane(obj=cq.Shape(md.load_step(sp)))
                    break
            else:
                print("找不到 model.step:", t); return
            uuid = t

    res = produce(shape, uuid, args.outdir, args.fastener,
                  add_washer=args.washer, add_nut=args.nut)
    if res:
        print(f"装配 {uuid}: {res['n_fasteners']} 处紧固件, "
              f"BOM {res['n_bom']} 项 -> {res['dir']}")


def produce(part_shape, uuid, outdir, fastener="socket",
            add_washer=True, add_nut=True, want_part_drawing=True,
            part_source=None, rerender_only=False, keep_script=False):
    """完整产出: 装配图(件号气泡+BOM) + 非标零件图。返回结果 dict 或 None。
    part_shape 应已是要用的位姿(真实毫米); 装配与投影共用同一位姿, 件号气泡对齐。

    rerender_only: 仅重出图(盘上已有带螺纹 model.step)。强制 lp.SIMPLE=True 让
    assemble 建光杆紧固件(make_screw 带螺纹 4.8s vs 光杆 0.1s, 慢 48 倍 —— 这是
    装配慢的真凶); 出图本就用光杆投影, 故画面一致。跳过 model.step/stl 重导出
    (不覆盖盘上带螺纹 3D 模型)。提速约 10 倍。"""
    import projlib
    import params as params_mod
    import match
    import drawing
    import library_parts as _lp
    _prev_simple = _lp.SIMPLE
    if rerender_only:
        _lp.SIMPLE = True
    try:
        return _produce_body(part_shape, uuid, outdir, fastener, add_washer,
                             add_nut, want_part_drawing, part_source,
                             rerender_only, projlib, drawing, keep_script)
    finally:
        _lp.SIMPLE = _prev_simple


def _produce_body(part_shape, uuid, outdir, fastener, add_washer, add_nut,
                  want_part_drawing, part_source, rerender_only, projlib, drawing,
                  keep_script=False):
    # 三维(STEP/STL/脚本)用**带螺纹**真实件; 工程图投影用**光杆简化**件 —— 带螺纹
    # 的螺旋面让 HLR 投影爆炸(单螺钉单视图 ~11s), 光杆投影才能保持出图速度。
    comp, report, anchors, recipe = assemble(part_shape, fastener, add_washer, add_nut)
    # 任意成功放置的库件都算数(螺钉套装 / 轴承 / 热熔嵌件)
    placed = [r for r in report if ("screw_size" in r or "part" in r)]
    if not placed:
        return None
    d = os.path.join(outdir, uuid)
    os.makedirs(d, exist_ok=True)
    if not rerender_only:
        cq.exporters.export(comp, os.path.join(d, "model.step"))
        cq.exporters.export(comp, os.path.join(d, "model.stl"))

    # ---- 自包含可重跑的装配脚本: 导入主体 + 按 recipe 造紧固件并摆放 ----
    # keep_script: 目录已有一份正确脚本(如 slim 目录的相对路径版), 只补其它模态。
    # 原目录写**内联自包含版**(与 build_assembly_variants 惯例一致, 无绝对路径)。
    if (not rerender_only) and (not keep_script) and part_source is not None:
        try:
            # 直接产 slim 相对路径版(从本目录 part/ 相对加载零件源码)。
            script = build_assembly_script(part_source, recipe)
            open(os.path.join(d, "assembly_cadquery.py"), "w",
                 encoding="utf-8").write(script)
            # 通用 helper(fasteners + library_parts)共享放在输出根目录(d 的上一级),
            # 不再复制进每个子目录。脚本头已把上一级加入 sys.path 解析它们。
            import shutil
            outroot = os.path.dirname(d)
            for hp in ("fasteners.py", "library_parts.py"):
                dst = os.path.join(outroot, hp)
                if not os.path.isfile(dst):
                    shutil.copyfile(os.path.join(HERE, hp), dst)
        except Exception as e:
            print("  [assembly script 跳过]", type(e).__name__, str(e)[:60])

    # ---- 装配图: 投影**光杆简化**装配体(带螺纹件投影会爆炸); 位姿与真实体一致 ----
    comp_simple = _recipe_compound(part_shape, recipe, simple=True)
    comp_shape = comp_simple.wrapped if hasattr(comp_simple, "wrapped") else comp_simple
    views = {n: projlib.project(comp_shape, p["paper_x"], p["paper_y"], deflection=0.1)
             for n, p in projlib.VIEWS.items()}
    bom, seeds = build_bom_and_balloons(part_shape, anchors)
    balloons = seeds_to_balloons(seeds, comp_shape)
    # ISO 128 点画线中心线: 紧固件回转轴 + 本体/所有回转体的圆特征中心十字。
    axes = build_fastener_axes(recipe, comp_simple)
    axes = axes + build_revolution_axes(comp_shape)
    # ISO 8826-1 轴承简化符号 + ISO 6410 螺纹约定线(均不改三维, 只在出图层叠加)。
    bearings = build_bearing_symbols(recipe)
    threads = build_thread_lines(recipe)
    # ISO 装配图: 不标任何尺寸(制造尺寸全部落在零件图), 也**不开剖视**(section=None) ——
    # 故"剖视中标准件不剖/不画剖面线"这条天然满足: 普通正交视图本就不画剖面线。
    # 只画视图 + 件号气泡 + BOM + 中心线 + 轴承符号 + 螺纹约定线。
    # Mass for the title block (grams) = body volume(mm^3) * steel density 7.85e-6 kg/mm^3.
    asm_mass = None
    try:
        from OCP.GProp import GProp_GProps as _GP
        from OCP.BRepGProp import BRepGProp as _BG
        # part_shape may be a cadquery Workplane / Shape wrapper or a raw TopoDS
        # shape; unwrap to the underlying OCP TopoDS_Shape before measuring.
        _sh = part_shape
        if hasattr(_sh, "val"):           # cadquery Workplane
            _sh = _sh.val()
        if hasattr(_sh, "wrapped"):       # cadquery Shape / Solid
            _sh = _sh.wrapped
        if hasattr(_sh, "toOCC"):
            _sh = _sh.toOCC()
        _pr = _GP(); _BG.VolumeProperties_s(_sh, _pr)
        asm_mass = _pr.Mass() * 7.85e-6 * 1000.0      # mm^3 -> g
    except Exception:
        asm_mass = None
    # Human-readable TITLE for the title block (ISO 7200) -- NOT the raw uuid/hash.
    # The dir name is "<uuid>__<Mtag>_<fastener>__asm"; derive "M4 socket assembly".
    _title = _readable_asm_title(uuid)
    drawing.render(views, uuid, os.path.join(d, "drawing"),
                   fmts=("png", "svg", "dxf"),
                   matched=[], overall=None, bom=bom, balloons=balloons, axes=axes,
                   bearings=bearings, threads=threads,
                   mass=asm_mass, title=_title)

    # ---- 非标零件图: 零件本体单独出图, 完整制造尺寸 ----
    # 复用 make_drawings.process: 它做姿态归一化 + 参数提取 + 几何匹配 + 完整
    # ISO 制造尺寸标注。零件本体放到 <d>/part/ 作为一个独立的 process 目标:
    # 需要 part/cadquery.py(参数来源) + part/model.step。
    if want_part_drawing and part_source is not None:
        pdir = os.path.join(d, "part")
        os.makedirs(pdir, exist_ok=True)
        # 零件脚本也去注释/空行(与装配脚本统一风格)
        open(os.path.join(pdir, "cadquery.py"), "w",
             encoding="utf-8").write(_strip_code(part_source))
        cq.exporters.export(part_shape, os.path.join(pdir, "model.step"))
        cq.exporters.export(part_shape, os.path.join(pdir, "model.stl"))
        try:
            import make_drawings as md
            md.OUT = d                            # process 在 <d> 下找 "part" 子目录
            md.process("part")                    # -> <d>/part/drawing.{png,svg,dxf}
        except Exception as e:
            print("  [part drawing 跳过]", type(e).__name__, str(e)[:60])

    json.dump({"part_uuid": uuid, "n_fasteners": len(placed),
               "bom": bom, "report": report},
              open(os.path.join(d, "assembly.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return {"dir": d, "n_fasteners": len(placed), "n_bom": len(bom)}


if __name__ == "__main__":
    main()
