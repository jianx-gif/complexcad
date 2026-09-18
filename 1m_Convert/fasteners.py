"""装配脚本用的紧固件工厂 + 摆放助手。让自动生成的装配脚本读起来与零件脚本同
一套 cadquery 风格:`fastener(kind, *args)` 造一个标准件, `place(part, axis,
point, seat, flip)` 把它对齐孔轴放到位。两者封装了 cq_warehouse 的细节与变换,
所以装配脚本本身只有命名变量 + 注释 + 调用, 干净可读、可独立 exec。
"""
import os
import sys
import math

import cadquery as cq

# cq_warehouse import 会全局替换 cadquery Shape 的 copy/fix/translate, 会搞坏零件
# 脚本里的 .shell()/.fix()。先备份, import 后恢复(摆放用原生 OCP 变换)。
_S = cq.occ_impl.shapes.Shape
_ORIG = {n: getattr(_S, n) for n in
         ("copy", "fix", "translate", "rotate", "located", "moved",
          "_apply_transform") if hasattr(_S, n)}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import library_parts as lp

for _n, _f in _ORIG.items():
    try:
        setattr(_S, _n, _f)
    except Exception:
        pass

from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir, gp_Vec
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform

_FACTORY = {
    "screw":   lambda a: lp.make_screw(*a)[0],
    "nut":     lambda a: lp.make_nut(*a)[0],
    "washer":  lambda a: lp.make_washer(*a)[0],
    "bearing": lambda a: lp.make_bearing(*a)[0],
    "heatset": lambda a: lp.make_heatset(*a)[0],
}


def fastener(kind, *args):
    """造一个标准件: kind in {screw,nut,washer,bearing,heatset}, args 见 library_parts。
    返回 cadquery Solid/Compound(造不出返回 None)。"""
    return _FACTORY[kind](args)


def place(part, axis, point, seat, flip=False):
    """把 part(默认 头/正面在 +Z、沿 -Z 延伸)对齐到孔轴 axis、放到轴向位置 seat。
    point 是孔轴上一点, seat 是沿轴的就位坐标; flip=True 先绕 X 翻 180 度(螺母/穿出
    端朝向相反)。用原生 OCP 变换, 避开 cq_warehouse 重写的 translate。"""
    if part is None:
        return None
    s = part.val() if hasattr(part, "val") else part
    td = s.wrapped if hasattr(s, "wrapped") else s
    a, p, t = axis, point, seat
    final = gp_Trsf()
    anchor = (p[0] + a[0]*t, p[1] + a[1]*t, p[2] + a[2]*t)
    tT = gp_Trsf(); tT.SetTranslation(gp_Vec(*anchor)); final.Multiply(tT)
    dot = max(-1.0, min(1.0, a[2])); ang = math.acos(dot)
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
    return cq.Shape(BRepBuilderAPI_Transform(td, final, True).Shape())
