"""cq_warehouse 库件扩展: 按孔径把零件的圆柱孔分配给不同库件 ——
  小孔(<= SCREW_MAX): 螺钉套装(多头型轮换)
  中孔(HEATSET 区间): 热熔螺纹嵌件 HeatSetNut
  大孔(>= BEARING_MIN, 按 OD 配): 深沟球/角接触/圆柱滚子/圆锥滚子轴承轮换
带中心轴孔的盘类零件: 链轮 sprocket(由 assemble 另行处理)。

这里只负责"给定一个孔(直径/轴/位置) -> 造出合适的库件对象 + BOM 元数据",
真正的对齐/平移仍由 assemble_fasteners.place() 完成。所有尺寸真实毫米。
"""
import math
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import cadquery as cq
from cq_warehouse.fastener import (
    SocketHeadCapScrew, HexHeadScrew, ButtonHeadScrew, PanHeadScrew,
    CheeseHeadScrew, CounterSunkScrew,
    HexNut, SquareNut, DomedCapNut, HexNutWithFlange, HeatSetNut,
    PlainWasher, ChamferedWasher,
)
from cq_warehouse.bearing import (
    SingleRowDeepGrooveBallBearing, SingleRowAngularContactBallBearing,
    SingleRowCylindricalRollerBearing, SingleRowTaperedRollerBearing,
)


# 紧固件是否生成真实 ISO 螺纹: False=带螺纹实体(慢几十倍、文件更大),
# True=光杆简化(快)。
# 用户要求(2026-06-26): **只有工程图用 ISO 简化画法, 其余(model.step/stl 3D 模型)
# 该带螺纹带螺纹**。故全局默认 False(3D 模型带真实螺纹)。简化只发生在两条**出图**
# 路径, 均为局部临时切换、不改全局/不动 3D 文件:
#   ① 正常出图投影: produce 内用 _recipe_compound(simple=True) 建光杆投影体(带螺纹
#      HLR 会爆炸), 叠加 build_thread_lines(ISO 6410 约定螺纹线)——图是简化画法。
#   ② rerender_only 重渲染: produce(rerender_only=True) 局部设 SIMPLE=True 加速装配,
#      并**跳过 model.step/stl 导出**, 故盘上带螺纹 3D 模型原样保留。
SIMPLE = False


def _obj(part):
    """cq_warehouse 件 -> cadquery Solid/Compound(去掉 cq_object 包装)。"""
    o = part.cq_object if hasattr(part, "cq_object") else part
    return o


# ---- 螺钉头型轮换: (类, fastener_type, iso_key) ---------------------------
SCREW_KINDS = [
    (SocketHeadCapScrew, "iso4762", "iso4762"),
    (HexHeadScrew,       "iso4014", "iso4014"),
    (ButtonHeadScrew,    "iso7380_1", "iso7380_1"),
    (PanHeadScrew,       "iso1580", "iso1580"),
    (CheeseHeadScrew,    "iso1207", "iso1207"),
    (CounterSunkScrew,   "iso10642", "iso10642"),
]
# ---- 螺母型轮换 ----------------------------------------------------------
NUT_KINDS = [
    (HexNut,          "iso4032", "iso4032"),
    (HexNutWithFlange, "din1665", "din1665"),
    (SquareNut,       "din557",  "din557"),
    (DomedCapNut,     "din1587", "din1587"),
]
# ---- 垫圈型轮换 ----------------------------------------------------------
WASHER_KINDS = [
    (PlainWasher,     "iso7089", "iso7089"),
    (ChamferedWasher, "iso7090", "iso7090"),
]
# ---- 轴承型轮换 ----------------------------------------------------------
BEARING_KINDS = [
    (SingleRowDeepGrooveBallBearing,     "SKT", "bearing_dgbb"),
    (SingleRowAngularContactBallBearing, "SKT", "bearing_acbb"),
    (SingleRowCylindricalRollerBearing,  "SKT", "bearing_crb"),
    (SingleRowTaperedRollerBearing,      "SKT", "bearing_trb"),
]

# 孔径分区(真实毫米)
SCREW_MAX = 13.0       # 螺钉套装上限
HEATSET_RANGE = (12.0, 16.0)   # 热熔嵌件区间(与螺钉略有交叠, 取最近)
BEARING_MIN = 15.0     # 轴承下限(按孔径 ~= 轴承外径 OD)


def make_screw(size, length, kind_idx=0):
    """按轮换下标造一个螺钉, 返回 (obj, iso_key)。失败回退到 socket。"""
    cls, ftype, iso_key = SCREW_KINDS[kind_idx % len(SCREW_KINDS)]
    try:
        return _obj(cls(size=size, length=length, fastener_type=ftype,
                        simple=SIMPLE)), iso_key
    except Exception:
        return _obj(SocketHeadCapScrew(size=size, length=length,
                    fastener_type="iso4762", simple=SIMPLE)), "iso4762"


def make_nut(size, mtag, kind_idx=0):
    cls, ftype, iso_key = NUT_KINDS[kind_idx % len(NUT_KINDS)]
    try:
        # flange/square/domed 多数用 'M8-1.25' 形式; square/domed 用 mtag 更稳
        sz = size if cls in (HexNut, HexNutWithFlange) else size
        return _obj(cls(size=sz, fastener_type=ftype, simple=SIMPLE)), iso_key
    except Exception:
        try:
            return _obj(HexNut(size=size, fastener_type="iso4032",
                        simple=SIMPLE)), "iso4032"
        except Exception:
            return None, None


def make_washer(mtag, kind_idx=0):
    cls, ftype, iso_key = WASHER_KINDS[kind_idx % len(WASHER_KINDS)]
    try:
        return _obj(cls(size=mtag, fastener_type=ftype)), iso_key
    except Exception:
        try:
            return _obj(PlainWasher(size=mtag, fastener_type="iso7089")), "iso7089"
        except Exception:
            return None, None


# ---- 热熔螺纹嵌件 --------------------------------------------------------
_HEATSET_SIZES = None


def _heatset_sizes():
    global _HEATSET_SIZES
    if _HEATSET_SIZES is None:
        out = []
        for s in HeatSetNut.sizes("Hilitchi"):
            # 'M4-0.7-8' -> (nominal, outer? ) 这里用嵌件外径需实例化, 先存原串
            m = s.split("-")
            try:
                out.append((float(m[0][1:]), s))    # (公称径, size串)
            except Exception:
                pass
        _HEATSET_SIZES = sorted(out)
    return _HEATSET_SIZES


def make_heatset(hole_dia):
    """按孔径选一个热熔嵌件(嵌件外径压入孔). 返回 (obj, iso_key, size串)。"""
    best = None
    for nominal, s in _heatset_sizes():
        # 嵌件外径略大于公称径; 用公称径 < 孔径 且最接近来选
        if nominal <= hole_dia + 0.2:
            err = abs(hole_dia - nominal)
            if best is None or err < best[0]:
                best = (err, s)
    if best is None:
        return None, None, None
    try:
        o = HeatSetNut(size=best[1], fastener_type="Hilitchi", simple=SIMPLE)
        return _obj(o), "heatset", best[1]
    except Exception:
        return None, None, None


# ---- 轴承(按孔径 ~ 外径 OD 选) ------------------------------------------
_BEARING_BY_OD = {}


def _bearing_sizes(cls, btype):
    key = (cls.__name__, btype)
    if key not in _BEARING_BY_OD:
        out = []
        try:
            for s in cls.sizes(btype):
                p = s.split("-")          # bore-OD-width
                try:
                    out.append((float(p[1]), s))      # (OD, size串)
                except Exception:
                    pass
        except Exception:
            pass
        _BEARING_BY_OD[key] = sorted(out)
    return _BEARING_BY_OD[key]


BEARING_FIT_TOL = 2.0      # 轴承外径与孔径之差需 <= 此值(过盈/紧配合), 否则不装


def make_bearing(hole_dia, kind_idx=0):
    """孔径 ~ 轴承外径 OD: 选 OD 最接近孔径(差 <= BEARING_FIT_TOL)的轴承。
    OD 必须接近孔径才是合理压入, 否则返回 None(不在过大孔里硬塞小轴承)。
    返回 (obj, iso_key, size串)。

    4 种轴承(深沟球/角接触/圆柱滚子/圆锥滚子)按 kind_idx **轮换分配**, 让数据集
    覆盖全部类型: 从 kind_idx 起依次尝试 4 种, 取**第一个能匹配该孔径**的类型
    (匹配=有 OD 在孔径 ±BEARING_FIT_TOL 内的尺寸)。不同孔/不同 pick 轮到不同类型,
    且某类型在该孔径无合适 OD 时自动用下一个能匹配的, 而非一律回退深沟球。"""
    n = len(BEARING_KINDS)
    for off in range(n):
        cls, btype, iso_key = BEARING_KINDS[(kind_idx + off) % n]
        sizes = _bearing_sizes(cls, btype)
        if not sizes:
            continue
        best = None
        for od, s in sizes:
            err = abs(hole_dia - od)
            if err <= BEARING_FIT_TOL and (best is None or err < best[0]):
                best = (err, s)
        if best is None:
            continue                      # 该类型在此孔径无合适 OD, 试下一种
        try:
            o = cls(size=best[1], bearing_type=btype)
            return _obj(o), iso_key, best[1]
        except Exception:
            continue                      # 造件失败, 试下一种
    return None, None, None               # 4 种都匹配不上 -> 不装轴承


def bearing_dims(size):
    """从轴承 size 串 'M10-30-9'(bore-OD-width) 解析 (bore, OD, width) mm。
    bore 段可能带 'M' 前缀, 去掉。"""
    p = size.split("-")
    bore = float(p[0].lstrip("Mm"))
    return bore, float(p[1]), float(p[2])


def make_bearing_iso(size):
    """ISO 8826 简化画法用的轴承几何: **不画滚珠/保持架**, 只用外圈+内圈两个同轴
    圆环实体(矩形截面)。投影后得到干净的矩形外廓 + OD/bore 圆, 即标准简化轮廓,
    没有真实滚珠的密集线条。用于工程图投影(不进 STEP, STEP 仍用真实轴承)。
    返回 cadquery 实体, 轴沿 +Z, 中心在原点(与真实轴承摆放参数一致)。"""
    bore, od, w = bearing_dims(size)
    ring_t = max(1.0, (od - bore) * 0.18)        # 圈壁厚度(外圈/内圈各一圈)
    outer = (cq.Workplane("XY").circle(od/2).circle(od/2 - ring_t).extrude(w))
    inner = (cq.Workplane("XY").circle(bore/2 + ring_t).circle(bore/2).extrude(w))
    ring = outer.union(inner).translate((0, 0, -w/2))   # 居中, 与 part_axial_extent 一致
    return ring


def part_axial_extent(obj):
    """库件沿自身 +Z 的 z 区间(放置前的本地), 供 assemble 算贴面位置。"""
    s = obj.val() if hasattr(obj, "val") else obj
    b = s.BoundingBox()
    return b.zmin, b.zmax


# ---- 链轮(大中心孔/凸台轴上) -------------------------------------------
from cq_warehouse.sprocket import Sprocket

SPROCKET_MIN_BORE = 30.0   # 链轮装在 >= 此孔径的中心轴孔上(超出轴承范围的大孔)
_STD_TEETH = [12, 14, 16, 18]


def make_sprocket(bore_dia, thickness, kind_idx=0):
    """在给定 bore_dia 的中心孔上造一个链轮(bore=孔径, 厚度贴料厚)。
    返回 (obj, iso_key, size串)。size 形如 'z16-p12.7'。"""
    teeth = _STD_TEETH[kind_idx % len(_STD_TEETH)]
    th = max(2.0, min(thickness, 8.0))
    try:
        s = Sprocket(num_teeth=teeth, chain_pitch=12.7, roller_diameter=7.75,
                     clearance=0.0, thickness=th,
                     bore_diameter=max(3.0, bore_dia))
        o = s.cq_object if hasattr(s, "cq_object") else s
        return o, "sprocket", f"z{teeth}-p12.7"
    except Exception:
        return None, None, None
