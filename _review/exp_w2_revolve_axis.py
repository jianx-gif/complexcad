# -*- coding: utf-8 -*-
"""实验W2: revolve 轴 测量器 (在 exp_w 的角度测量之外, 再测回转轴).

对每个含 .revolve( 的模型 (来自 exp_w 的记录列表, 1844 个):
  声明侧: 用 ast 解析 cadquery.py, 找到每个 .revolve( 调用, 沿链回溯到 cq.Workplane(...)
          (允许经过模块级唯一赋值的变量), 仅接受 平面相关调用 workplane()/center()/transformed()
          + 纯草图调用; 其它 (选择器/循环/函数/布尔/未知) 一律判 "not statically resolvable".
          平面运算不自己算, 而是在真实 cq.Workplane 上重放这些调用, 再按 CadQuery 2.6.1
          Workplane.revolve 的源码把 axisStart/axisEnd (默认 (0,0)->(0,1), 局部坐标) 经
          plane.toWorldCoords 变成全局 3D 直线 (点 + 单位方向).
  实测侧: 读 model.brep, 取回转类面 (Cylinder/Cone/Torus/SurfaceOfRevolution) 的 gp_Ax1 与面积;
          面积最大者为 "主轴"; 统计与主轴共线的面数 (|cos|>=0.999 且 线距<=0.01mm).
  比较:   方向匹配 |cos|>=0.999 (方向不分正负); 直线匹配 = 方向匹配 且 平行线间距 <= 0.01mm.
          另记声明轴是否与 任一 回转面共线 (用于归因: 主面是别的特征 vs 回转体已被后续布尔改掉).
  纯净子集: 单次 revolve 且程序中链外没有会产生圆柱/回转面的操作.
用法: python exp_w2_revolve_axis.py [n] [--sample N --seed 42]
输出: _review/exp_w2_revolve_axis.json + exp_w2_revolve_axis_records.jsonl
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import sys, os, re, json, math, time, ast, random, collections

ROOT = _ROOT
OUT = os.path.join(ROOT, 'output')
REV_DIR = os.path.join(ROOT, '_review')

import cadquery as cq
from OCP.BRep import BRep_Builder
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import (GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Torus,
                         GeomAbs_SurfaceOfRevolution)
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

COS_TOL = 0.999
DIST_TOL = 0.01

# ----------------------------------------------------------------------------- static resolver
SKETCH_OK = {
    'moveTo', 'lineTo', 'line', 'vLine', 'hLine', 'vLineTo', 'hLineTo', 'polarLine', 'polarLineTo',
    'threePointArc', 'radiusArc', 'sagittaArc', 'tangentArcPoint', 'spline', 'polyline', 'close',
    'rect', 'circle', 'ellipse', 'ellipseArc', 'polygon', 'slot2D', 'mirrorX', 'mirrorY', 'wire',
    'consolidateWires', 'toPending', 'tag', 'bezier', 'pushPoints', 'rarray', 'polarArray',
    # 只改栈上对象, 不改 plane (revolve 的轴只由 plane 决定)
    'translate', 'rotate', 'mirror',
}
PLANE_OPS = {'workplane', 'center', 'transformed'}
NESTING = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.For, ast.While, ast.If,
           ast.With, ast.Try, ast.Lambda, ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)


class Unresolvable(Exception):
    pass


class Program:
    """模块级静态求值环境."""

    def __init__(self, src):
        self.tree = ast.parse(src)
        self.parent = {}
        for node in ast.walk(self.tree):
            for ch in ast.iter_child_nodes(node):
                self.parent[ch] = node
        # 全模块出现的赋值名计数 (含嵌套/循环/增广/for 目标), 用于唯一性判断
        self.assign_count = collections.Counter()
        self.top_assign = {}  # name -> (lineno, value node)  仅模块级简单 Assign
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    for n in ast.walk(t):
                        if isinstance(n, ast.Name):
                            self.assign_count[n.id] += 1
                if (self.parent.get(node) is self.tree and len(node.targets) == 1
                        and isinstance(node.targets[0], ast.Name)):
                    self.top_assign[node.targets[0].id] = (node.lineno, node.value)
            elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
                for n in ast.walk(node.target):
                    if isinstance(n, ast.Name):
                        self.assign_count[n.id] += 1
            elif isinstance(node, (ast.For, ast.comprehension)):
                for n in ast.walk(node.target):
                    if isinstance(n, ast.Name):
                        self.assign_count[n.id] += 1
            elif isinstance(node, ast.NamedExpr):
                self.assign_count[node.target.id] += 1
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.assign_count[node.name] += 1
        self.math_names = {}
        for node in self.tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == 'math':
                for a in node.names:
                    if a.name == '*':
                        for k in dir(math):
                            if not k.startswith('_'):
                                self.math_names[k] = getattr(math, k)
                    elif hasattr(math, a.name):
                        self.math_names[a.asname or a.name] = getattr(math, a.name)
        self.cache = {}

    def is_top_level(self, node):
        p = self.parent.get(node)
        while p is not None and p is not self.tree:
            if isinstance(p, NESTING):
                return False
            p = self.parent.get(p)
        return True

    def stmt_of(self, node):
        p = node
        while self.parent.get(p) is not self.tree:
            p = self.parent[p]
        return p

    def name_value(self, name, before_line):
        """模块级唯一赋值且在 before_line 之前, 返回其 value 节点."""
        if self.assign_count[name] != 1 or name not in self.top_assign:
            raise Unresolvable('name_not_unique_or_not_toplevel:' + name)
        ln, val = self.top_assign[name]
        if ln >= before_line:
            raise Unresolvable('name_assigned_after_use:' + name)
        return val

    def ev(self, node, before_line, depth=0):
        if depth > 40:
            raise Unresolvable('eval_depth')
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float, bool, str)) or node.value is None:
                return node.value
            raise Unresolvable('const_type')
        if isinstance(node, ast.Name):
            if node.id in ('True', 'False', 'None'):
                return {'True': True, 'False': False, 'None': None}[node.id]
            if node.id in self.math_names:
                return self.math_names[node.id]
            key = (node.id, before_line)
            if key in self.cache:
                return self.cache[key]
            val = self.name_value(node.id, before_line)
            ln = self.top_assign[node.id][0]
            v = self.ev(val, ln, depth + 1)
            self.cache[key] = v
            return v
        if isinstance(node, ast.UnaryOp):
            v = self.ev(node.operand, before_line, depth + 1)
            if isinstance(node.op, ast.USub):
                return -v
            if isinstance(node.op, ast.UAdd):
                return +v
            if isinstance(node.op, ast.Not):
                return not v
            raise Unresolvable('unary')
        if isinstance(node, ast.BinOp):
            a = self.ev(node.left, before_line, depth + 1)
            b = self.ev(node.right, before_line, depth + 1)
            op = type(node.op)
            try:
                if op is ast.Add: return a + b
                if op is ast.Sub: return a - b
                if op is ast.Mult: return a * b
                if op is ast.Div: return a / b
                if op is ast.FloorDiv: return a // b
                if op is ast.Mod: return a % b
                if op is ast.Pow: return a ** b
            except Exception as e:
                raise Unresolvable('arith:' + type(e).__name__)
            raise Unresolvable('binop')
        if isinstance(node, (ast.Tuple, ast.List)):
            return tuple(self.ev(e, before_line, depth + 1) for e in node.elts)
        if isinstance(node, ast.Subscript):
            base = self.ev(node.value, before_line, depth + 1)
            idx = self.ev(node.slice, before_line, depth + 1)
            try:
                return base[idx]
            except Exception:
                raise Unresolvable('subscript')
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == 'math' and hasattr(math, node.attr):
                return getattr(math, node.attr)
            raise Unresolvable('attribute:' + node.attr)
        if isinstance(node, ast.Call):
            f = node.func
            args = [self.ev(a, before_line, depth + 1) for a in node.args]
            kwargs = {k.arg: self.ev(k.value, before_line, depth + 1) for k in node.keywords if k.arg}
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                if f.value.id == 'math' and hasattr(math, f.attr):
                    return getattr(math, f.attr)(*args, **kwargs)
                if f.value.id in ('cq', 'cadquery'):
                    if f.attr == 'Vector':
                        v = cq.Vector(*args) if args else cq.Vector()
                        return v.toTuple()
                    if f.attr == 'Plane':
                        return cq.Plane(*args, **kwargs)
                    raise Unresolvable('cq_call:' + f.attr)
            if (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Attribute)
                    and isinstance(f.value.value, ast.Name) and f.value.value.id in ('cq', 'cadquery')
                    and f.value.attr == 'Plane' and f.attr == 'named'):
                return cq.Plane.named(*args, **kwargs)
            if isinstance(f, ast.Name):
                if f.id in ('int', 'float', 'abs', 'min', 'max', 'round', 'tuple', 'list'):
                    return {'int': int, 'float': float, 'abs': abs, 'min': min, 'max': max,
                            'round': round, 'tuple': tuple, 'list': tuple}[f.id](*args, **kwargs)
                if f.id in self.math_names:
                    return self.math_names[f.id](*args, **kwargs)
            raise Unresolvable('call:' + ast.dump(f)[:40])
        raise Unresolvable('node:' + type(node).__name__)


def is_workplane_ctor(call):
    f = call.func
    if isinstance(f, ast.Attribute) and f.attr == 'Workplane' and isinstance(f.value, ast.Name) \
            and f.value.id in ('cq', 'cadquery'):
        return True
    if isinstance(f, ast.Name) and f.id == 'Workplane':
        return True
    return False


def walk_chain(prog, expr, before_line, depth=0):
    """回溯 expr 到 cq.Workplane(...) 根; 返回 (root_call, [ (method, call) ...] 自根到 expr 的顺序)."""
    if depth > 20:
        raise Unresolvable('chain_depth')
    ops = []
    e = expr
    while True:
        if isinstance(e, ast.Call):
            if is_workplane_ctor(e):
                ops.reverse()
                return e, ops
            if isinstance(e.func, ast.Attribute):
                ops.append((e.func.attr, e))
                e = e.func.value
                continue
            raise Unresolvable('root_call:' + ast.dump(e.func)[:40])
        if isinstance(e, ast.Name):
            val = prog.name_value(e.id, before_line)
            ln = prog.top_assign[e.id][0]
            root, ops2 = walk_chain(prog, val, ln, depth + 1)
            ops.reverse()
            return root, ops2 + ops
        if isinstance(e, ast.Attribute):
            raise Unresolvable('root_attribute:' + e.attr)
        raise Unresolvable('root_node:' + type(e).__name__)


def call_args(prog, call, before_line, names):
    """按位置参数名列表 names 把实参解析为 dict."""
    out = {}
    for i, a in enumerate(call.args):
        if i >= len(names):
            raise Unresolvable('too_many_args')
        out[names[i]] = prog.ev(a, before_line)
    for k in call.keywords:
        if k.arg is None:
            raise Unresolvable('star_kwargs')
        out[k.arg] = prog.ev(k.value, before_line)
    return out


def resolve_plane(prog, root, ops, before_line):
    """在真实 cq.Workplane 上重放 平面相关调用, 返回 (plane, info)."""
    ra = call_args(prog, root, before_line, ['inPlane', 'origin', 'obj'])
    if 'obj' in ra:
        raise Unresolvable('workplane_obj_kw')
    in_plane = ra.get('inPlane', 'XY')
    origin = ra.get('origin', (0, 0, 0))
    if isinstance(in_plane, str):
        try:
            wp = cq.Workplane(in_plane, origin=tuple(float(x) for x in origin))
        except Exception as e:
            raise Unresolvable('workplane_ctor:' + str(e)[:40])
    elif isinstance(in_plane, cq.Plane):
        wp = cq.Workplane(in_plane)
    else:
        raise Unresolvable('workplane_arg_type')
    info = dict(named=in_plane if isinstance(in_plane, str) else 'Plane()',
                n_plane_ops=0, chain_ops=[m for m, _ in ops])
    for m, call in ops:
        if m in SKETCH_OK:
            continue
        if m not in PLANE_OPS:
            raise Unresolvable('chain_op:' + m)
        info['n_plane_ops'] += 1
        if m == 'workplane':
            kw = call_args(prog, call, before_line, ['offset', 'invert', 'centerOption', 'origin'])
            if kw.get('centerOption', 'ProjectedOrigin') != 'ProjectedOrigin':
                raise Unresolvable('workplane_centerOption')
            wp = wp.workplane(offset=float(kw.get('offset', 0.0)), invert=bool(kw.get('invert', False)),
                              origin=kw.get('origin'))
        elif m == 'center':
            kw = call_args(prog, call, before_line, ['x', 'y'])
            wp = wp.center(float(kw['x']), float(kw['y']))
        elif m == 'transformed':
            kw = call_args(prog, call, before_line, ['rotate', 'offset'])
            rot = tuple(float(x) for x in kw.get('rotate', (0, 0, 0)))
            off = tuple(float(x) for x in kw.get('offset', (0, 0, 0)))
            wp = wp.transformed(rotate=rot, offset=off)
    return wp.plane, info


def as_vec_like(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        raise Unresolvable('axis_scalar')
    t = tuple(float(x) for x in v)
    if len(t) not in (2, 3):
        raise Unresolvable('axis_len')
    return t


def declared_axis(plane, axisStart, axisEnd):
    """逐行复刻 cadquery 2.6.1 Workplane.revolve 的轴计算."""
    quirk = False
    if axisStart is None:
        s = plane.toWorldCoords((0, 0)).toTuple()
    else:
        s = plane.toWorldCoords(axisStart).toTuple()
    if axisEnd is None:
        if s[1] != 0:
            e = plane.toWorldCoords((0, s[1])).toTuple()
            quirk = True
        else:
            e = plane.toWorldCoords((0, 1)).toTuple()
    else:
        e = plane.toWorldCoords(axisEnd).toTuple()
    d = (e[0] - s[0], e[1] - s[1], e[2] - s[2])
    n = math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)
    if n < 1e-9:
        raise Unresolvable('axis_degenerate')
    return tuple(s), (d[0] / n, d[1] / n, d[2] / n), quirk


POST_XFORM = ('translate', 'rotate', 'mirror', 'rotateAboutCenter')


def post_transform_ops(prog, call, stmt, src):
    """revolve 之后 该结果是否被 translate/rotate/mirror 搬动 (同一表达式向上, 或 赋值变量在后文被搬动).
    返回检测到的方法名列表 (空 = 未检测到)."""
    found = []
    node = call
    while True:
        p = prog.parent.get(node)
        if isinstance(p, ast.Attribute) and p.value is node:
            q = prog.parent.get(p)
            if isinstance(q, ast.Call) and q.func is p:
                if p.attr in POST_XFORM:
                    found.append(p.attr)
                node = q
                continue
        break
    if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
        name = stmt.targets[0].id
        rest = '\n'.join(src.split('\n')[getattr(stmt, 'end_lineno', stmt.lineno):])
        for m in re.finditer(r'\b%s\s*\.\s*(translate|rotate|mirror|rotateAboutCenter)\s*\(' % re.escape(name), rest):
            found.append(m.group(1))
    return found


def declared_calls(src):
    """返回每个 .revolve( 调用的解析结果列表 (按源码顺序)."""
    try:
        prog = Program(src)
    except SyntaxError:
        return [dict(ok=False, reason='syntax_error', line=0)]
    calls = [n for n in ast.walk(prog.tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'revolve']
    calls.sort(key=lambda n: (n.lineno, n.col_offset))
    out = []
    for c in calls:
        rec = dict(line=c.lineno)
        try:
            if not prog.is_top_level(c):
                raise Unresolvable('revolve_nested')
            stmt = prog.stmt_of(c)
            before = stmt.lineno
            root, ops = walk_chain(prog, c.func.value, before)
            plane, info = resolve_plane(prog, root, ops, before)
            a = call_args(prog, c, before, ['angleDegrees', 'axisStart', 'axisEnd', 'combine', 'clean'])
            s, d, quirk = declared_axis(plane, as_vec_like(a.get('axisStart')), as_vec_like(a.get('axisEnd')))
            ang = a.get('angleDegrees', 360.0)
            zd = plane.zDir.toTuple()
            perp = abs(d[0] * zd[0] + d[1] * zd[1] + d[2] * zd[2])
            rec.update(ok=True, point=[round(x, 6) for x in s], dir=[round(x, 6) for x in d],
                       angle=(float(ang) if isinstance(ang, (int, float)) else None),
                       axis_explicit=('axisStart' in a or 'axisEnd' in a), axisend_quirk=quirk,
                       # 声明轴垂直于草图平面 => OCCT 回转退化 (体积 0), CadQuery 不报错
                       axis_perp_to_plane=perp >= COS_TOL,
                       post_transform=post_transform_ops(prog, c, stmt, src),
                       plane=info['named'], n_plane_ops=info['n_plane_ops'],
                       chain_ops=info['chain_ops'],
                       plane_origin=[round(x, 6) for x in plane.origin.toTuple()],
                       plane_zdir=[round(x, 6) for x in zd])
        except Unresolvable as e:
            rec.update(ok=False, reason=str(e))
        except Exception as e:
            rec.update(ok=False, reason='exc:' + type(e).__name__ + ':' + str(e)[:50])
        out.append(rec)
    return out


# ----------------------------------------------------------------------------- measured side
TYPE_NAME = {GeomAbs_Cylinder: 'cylinder', GeomAbs_Cone: 'cone', GeomAbs_Torus: 'torus',
             GeomAbs_SurfaceOfRevolution: 'revolution'}


def measured_faces(brep_path):
    shape = TopoDS_Shape()
    if not BRepTools.Read_s(shape, brep_path, BRep_Builder()):
        return None
    faces = []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current())
        ad = BRepAdaptor_Surface(f)
        t = ad.GetType()
        if t in TYPE_NAME:
            try:
                if t == GeomAbs_Cylinder:
                    ax = ad.Cylinder().Axis()
                elif t == GeomAbs_Cone:
                    ax = ad.Cone().Axis()
                elif t == GeomAbs_Torus:
                    ax = ad.Torus().Axis()
                else:
                    ax = ad.AxeOfRevolution()
                p, d = ax.Location(), ax.Direction()
                props = GProp_GProps()
                BRepGProp.SurfaceProperties_s(f, props)
                faces.append(dict(type=TYPE_NAME[t], area=props.Mass(),
                                  point=(p.X(), p.Y(), p.Z()), dir=(d.X(), d.Y(), d.Z())))
            except Exception:
                pass
        ex.Next()
    return faces


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _norm(a):
    return math.sqrt(_dot(a, a))


def line_compare(p1, d1, p2, d2):
    """返回 (abs_cos, angle_deg in [0,90], offset_mm).
    offset: 平行时 = 两平行线的垂直距离 (连线去掉沿方向分量); 不平行时 = 两直线最近距离."""
    c = abs(_dot(d1, d2))
    c = min(1.0, c)
    ang = math.degrees(math.acos(c))
    w = _sub(p2, p1)
    if c >= COS_TOL:
        proj = _dot(w, d1)
        perp = _sub(w, (d1[0] * proj, d1[1] * proj, d1[2] * proj))
        off = _norm(perp)
    else:
        n = _cross(d1, d2)
        nn = _norm(n)
        off = abs(_dot(w, n)) / nn if nn > 1e-12 else 0.0
    return c, ang, off


def analyse_measured(faces):
    if not faces:
        return None
    faces = sorted(faces, key=lambda f: -f['area'])
    principal = faces[0]
    coax = 0
    for f in faces:
        c, ang, off = line_compare(principal['point'], principal['dir'], f['point'], f['dir'])
        if c >= COS_TOL and off <= DIST_TOL:
            coax += 1
    return principal, coax, faces


# ----------------------------------------------------------------------------- pure-subset classification
CYL_OPS_CORE = ['.circle(', '.hole(', '.cboreHole(', '.cskHole(', '.cylinder(', '.sphere(', '.ellipse(',
                '.slot2D(', '.sweep(', '.loft(', '.shell(', 'makeCylinder(', 'makeSphere(', 'makeTorus(',
                'makeCone(', '.text(', '.ellipseArc(']
CYL_OPS_BLEND = ['.fillet(', '.chamfer(']


def purity(src, decl):
    """单 revolve 且 链外无 产生回转面的操作. 返回 dict(pure_relaxed, pure_strict)."""
    if len(decl) != 1 or not decl[0].get('ok'):
        return dict(pure_relaxed=False, pure_strict=False)
    chain = collections.Counter(decl[0]['chain_ops'])

    def outside(op_list):
        for op in op_list:
            name = op.split('(')[0].lstrip('.')
            n_src = src.count(op)
            n_chain = chain.get(name, 0) if op.startswith('.') else 0
            if n_src - n_chain > 0:
                return True
        return False
    relaxed = not outside(CYL_OPS_CORE)
    strict = relaxed and not outside(CYL_OPS_BLEND)
    return dict(pure_relaxed=relaxed, pure_strict=strict)


# ----------------------------------------------------------------------------- per model
def run(uuid):
    py = os.path.join(OUT, uuid, 'cadquery.py')
    br = os.path.join(OUT, uuid, 'model.brep')
    if not (os.path.isfile(py) and os.path.isfile(br)):
        return dict(uuid=uuid, error='missing_files')
    src = open(py, encoding='utf-8', errors='replace').read()
    decl = declared_calls(src)
    if not decl:
        return dict(uuid=uuid, error='no_revolve_call')
    faces = measured_faces(br)
    if faces is None:
        return dict(uuid=uuid, error='brep_read')
    rec = dict(uuid=uuid, n_calls=len(decl), n_rev_faces=len(faces), calls=decl)
    rec.update(purity(src, decl))
    m = analyse_measured(faces)
    if m is None:
        rec.update(principal=None, coaxial_count=0, faces=[])
    else:
        principal, coax, sfaces = m
        rec.update(principal=dict(type=principal['type'], area=round(principal['area'], 4),
                                  point=[round(x, 6) for x in principal['point']],
                                  dir=[round(x, 6) for x in principal['dir']]),
                   coaxial_count=coax,
                   faces=[dict(type=f['type'], area=round(f['area'], 4),
                               point=[round(x, 4) for x in f['point']],
                               dir=[round(x, 5) for x in f['dir']]) for f in sfaces])
    for c in decl:
        if not c.get('ok'):
            continue
        if m is None:
            c.update(no_candidate=True)
            continue
        principal, coax, sfaces = m
        cosv, ang, off = line_compare(principal['point'], principal['dir'], c['point'], c['dir'])
        c.update(no_candidate=False, abs_cos=round(cosv, 8), angle_dev_deg=round(ang, 6),
                 line_offset_mm=round(off, 6), dir_match=cosv >= COS_TOL,
                 line_match=(cosv >= COS_TOL and off <= DIST_TOL))
        # 归因辅助: 声明轴是否与任一回转面共线 / 同向
        best_rank, best_type, any_dir = None, None, False
        for rank, f in enumerate(sfaces):
            cf, af, of = line_compare(f['point'], f['dir'], c['point'], c['dir'])
            if cf >= COS_TOL:
                any_dir = True
                if of <= DIST_TOL and best_rank is None:
                    best_rank, best_type = rank, f['type']
        c.update(any_face_dir_match=any_dir, any_face_line_match=best_rank is not None,
                 best_face_rank=best_rank, best_face_type=best_type,
                 best_face_area=(round(sfaces[best_rank]['area'], 4) if best_rank is not None else None),
                 principal_type=principal['type'], principal_area=round(principal['area'], 4))
    return rec


# ----------------------------------------------------------------------------- summary
def dist(values, edges):
    """按区间边界统计: 返回 bins + 基本统计量 + 最常见取值."""
    values = sorted(values)
    out = collections.OrderedDict()
    labels = []
    for i in range(len(edges) - 1):
        labels.append('[%g,%g)' % (edges[i], edges[i + 1]))
    labels.append('>=%g' % edges[-1])
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
        stats.update(min=values[0], median=values[len(values) // 2], max=values[-1],
                     mean=round(sum(values) / len(values), 6))
    return dict(bins=out, stats=stats,
                top_values=[[v, n] for v, n in collections.Counter(round(v, 4) for v in values).most_common(8)])


def summarize(recs, subset_name, pred):
    """pred(rec, call) -> bool 选择纳入的 (模型, 调用) 对."""
    S = collections.Counter()
    ang_dev, off_dev, off_dirmatch_all = [], [], []
    reasons = collections.Counter()
    mism = []
    model_any = collections.Counter()
    for r in recs:
        if 'error' in r:
            continue
        m_att = m_res = m_dir = m_line = m_noc = False
        for c in r['calls']:
            if not pred(r, c):
                continue
            S['attempted_calls'] += 1
            m_att = True
            if not c['ok']:
                reasons[c['reason'].split(':')[0]] += 1
                S['not_resolvable_calls'] += 1
                continue
            S['resolvable_calls'] += 1
            m_res = True
            if c['no_candidate']:
                S['no_candidate_calls'] += 1
                m_noc = True
                continue
            S['compared_calls'] += 1
            if c['dir_match']:
                S['dir_match_calls'] += 1
                m_dir = True
                off_dirmatch_all.append(c['line_offset_mm'])
                if c['line_match']:
                    S['line_match_calls'] += 1
                    m_line = True
                else:
                    S['dir_match_line_mismatch_calls'] += 1
                    off_dev.append(c['line_offset_mm'])
                    mism.append((r['uuid'], c))
            else:
                S['dir_mismatch_calls'] += 1
                ang_dev.append(c['angle_dev_deg'])
                mism.append((r['uuid'], c))
            if c.get('any_face_line_match'):
                S['any_face_line_match_calls'] += 1
            if c.get('any_face_dir_match'):
                S['any_face_dir_match_calls'] += 1
            if c.get('axisend_quirk'):
                S['axisend_quirk_calls'] += 1
            if c.get('axis_explicit'):
                S['axis_explicit_calls'] += 1
        if m_att:
            model_any['attempted_models'] += 1
        if m_res:
            model_any['resolvable_models'] += 1
        if m_noc and not m_dir:
            model_any['no_candidate_models'] += 1
        if m_dir:
            model_any['dir_match_models'] += 1
        if m_line:
            model_any['line_match_models'] += 1
    res = S['resolvable_calls']
    comp = S['compared_calls']
    rates = {}
    if res:
        rates = dict(dir_match_pct_of_resolvable=round(100.0 * S['dir_match_calls'] / res, 3),
                     line_match_pct_of_resolvable=round(100.0 * S['line_match_calls'] / res, 3),
                     no_candidate_pct_of_resolvable=round(100.0 * S['no_candidate_calls'] / res, 3))
    if comp:
        rates.update(dir_match_pct_of_compared=round(100.0 * S['dir_match_calls'] / comp, 3),
                     line_match_pct_of_compared=round(100.0 * S['line_match_calls'] / comp, 3))
    mres = model_any['resolvable_models']
    if mres:
        rates.update(dir_match_models_pct=round(100.0 * model_any['dir_match_models'] / mres, 3),
                     line_match_models_pct=round(100.0 * model_any['line_match_models'] / mres, 3))
    # 不匹配归因 (自动部分)
    attrib = collections.Counter()
    attrib2 = collections.Counter()
    for u, c in mism:
        if c['dir_match']:
            key = 'parallel_offset:' + ('declared_axis_is_smaller_face' if c['any_face_line_match'] else 'no_face_on_declared_line')
        else:
            key = 'direction:' + ('declared_axis_is_smaller_face' if c['any_face_line_match'] else
                                  ('parallel_face_exists_but_offset' if c['any_face_dir_match'] else 'no_face_on_declared_axis'))
        attrib[key] += 1
        # 优先级归因: 退化轴 > 回转后搬动 > 主面是别的特征(声明轴仍在小面上) > 声明轴无任何面
        if c.get('axis_perp_to_plane'):
            k2 = 'A_declared_axis_perpendicular_to_sketch_plane(degenerate_revolve)'
        elif c.get('post_transform'):
            k2 = 'B_body_translated_or_rotated_after_revolve'
        elif c['any_face_line_match']:
            k2 = 'C_principal_face_is_another_feature(declared_axis_present_on_smaller_face)'
        elif c['any_face_dir_match']:
            k2 = 'D_no_face_on_declared_line(parallel_face_elsewhere)'
        else:
            k2 = 'E_no_face_on_declared_axis'
        attrib2[k2] += 1
    S['axis_perp_to_plane_calls'] = sum(1 for r in recs if 'error' not in r for c in r['calls']
                                        if pred(r, c) and c.get('ok') and c.get('axis_perp_to_plane'))
    S['post_transform_calls'] = sum(1 for r in recs if 'error' not in r for c in r['calls']
                                    if pred(r, c) and c.get('ok') and c.get('post_transform'))
    return dict(subset=subset_name, counts=dict(S), models=dict(model_any), rates=rates,
                not_resolvable_reasons=dict(reasons.most_common()),
                angle_deviation_deg_of_dir_mismatches=dist(ang_dev, [0, 0.1, 1, 5, 30, 60, 89, 89.999]),
                line_offset_mm_of_dir_match_line_mismatches=dist(off_dev, [0, 0.01, 0.1, 1, 10, 100]),
                line_offset_mm_of_all_dir_matches=dist(off_dirmatch_all, [0, 1e-6, 1e-3, 0.01, 0.1, 1, 10, 100]),
                mismatch_attribution=dict(attrib.most_common()),
                mismatch_attribution_prioritized=dict(attrib2.most_common()),
                mismatch_examples=[dict(uuid=u, line=c['line'], angle_dev_deg=c['angle_dev_deg'],
                                        axis_perp_to_plane=c.get('axis_perp_to_plane'), post_transform=c.get('post_transform'),
                                        line_offset_mm=c['line_offset_mm'], declared_dir=c['dir'],
                                        declared_point=c['point'], plane=c['plane'],
                                        principal_type=c['principal_type'], principal_area=c['principal_area'],
                                        any_face_line_match=c['any_face_line_match'],
                                        best_face_rank=c['best_face_rank'], best_face_type=c['best_face_type'],
                                        best_face_area=c['best_face_area'])
                                   for u, c in mism[:40]])


if __name__ == '__main__':
    t0 = time.time()
    args = sys.argv[1:]
    N = 0
    sample = 0
    seed = 42
    i = 0
    while i < len(args):
        if args[i] == '--sample':
            sample = int(args[i + 1]); i += 2
        elif args[i] == '--seed':
            seed = int(args[i + 1]); i += 2
        else:
            N = int(args[i]); i += 1
    uuids = [json.loads(l)['uuid'].strip() for l in
             open(os.path.join(REV_DIR, 'exp_w_revolve_records.jsonl'), encoding='utf-8') if l.strip()]
    total_pop = len(uuids)
    if sample:
        random.seed(seed)
        uuids = random.sample(uuids, sample)
    if N:
        uuids = uuids[:N]
    recs = []
    fo = open(os.path.join(REV_DIR, 'exp_w2_revolve_axis_records.jsonl'), 'w', encoding='utf-8')
    for i, u in enumerate(uuids, 1):
        try:
            r = run(u)
        except Exception as e:
            r = dict(uuid=u, error='fatal:' + type(e).__name__ + ':' + str(e)[:80])
        recs.append(r)
        fo.write(json.dumps(r) + '\n')
        if i % 200 == 0:
            print(i, '/', len(uuids), '%.0fs' % (time.time() - t0), flush=True)
    fo.close()
    ok = [r for r in recs if 'error' not in r]
    summary = dict(
        population_models=total_pop, sample_size=len(uuids), seed=(seed if sample else None),
        n_models_ok=len(ok), n_models_error=len(recs) - len(ok),
        errors=dict(collections.Counter(r['error'].split(':')[0] for r in recs if 'error' in r)),
        tolerances=dict(abs_cos_min=COS_TOL, line_dist_max_mm=DIST_TOL),
        n_calls_per_model=dict(collections.Counter(r['n_calls'] for r in ok)),
        models_without_revolved_faces=sum(1 for r in ok if r['n_rev_faces'] == 0),
        principal_face_type=dict(collections.Counter(r['principal']['type'] for r in ok if r['principal'])),
        coaxial_count_hist=dict(collections.Counter(min(r['coaxial_count'], 20) for r in ok)),
        coaxial_all_faces_models=sum(1 for r in ok if r['n_rev_faces'] and r['coaxial_count'] == r['n_rev_faces']),
        plane_named=dict(collections.Counter(c['plane'] for r in ok for c in r['calls'] if c.get('ok'))),
        n_plane_ops_hist=dict(collections.Counter(c['n_plane_ops'] for r in ok for c in r['calls'] if c.get('ok'))),
        pure_relaxed_models=sum(1 for r in ok if r['pure_relaxed']),
        pure_strict_models=sum(1 for r in ok if r['pure_strict']),
        all_calls=summarize(ok, 'all revolve calls', lambda r, c: True),
        single_call_models=summarize(ok, 'models with exactly one revolve call', lambda r, c: r['n_calls'] == 1),
        pure_relaxed=summarize(ok, 'single revolve, no circle/hole/cbore/csk/cylinder/sphere/ellipse/slot/sweep/loft/shell/text outside the chain (fillet/chamfer allowed)',
                               lambda r, c: r['pure_relaxed']),
        pure_strict=summarize(ok, 'pure_relaxed and also no fillet/chamfer', lambda r, c: r['pure_strict']),
        runtime_s=round(time.time() - t0, 1),
    )
    json.dump(summary, open(os.path.join(REV_DIR, 'exp_w2_revolve_axis.json'), 'w', encoding='utf-8'), indent=1)
    print(json.dumps(summary, indent=1))
