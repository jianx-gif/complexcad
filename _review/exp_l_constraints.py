# -*- coding: utf-8 -*-
"""实验L (v6): 把显式位姿装配脚本改写为 **基于 cq.Assembly 约束的可运行 CadQuery 脚本**.

对每个装配目录 <dir>/assembly_cadquery.py (零件用显式刚体变换 place(...) 摆放):
  1. 执行原脚本, 记录每个标准件的 fastener(...) 参数与 place(...) 位姿;
  2. 在已摆放几何上几何检测接触面对 (座面 ∥ 轴、反法向、共站、相触) 及同轴圆边;
  3. 把接触面对映射回各零件的局部坐标系, 得到 Axis(反平行法向)+Point(圆心重合) 配合;
  4. 生成 <dir>/assembly_constrained_cadquery.py —— 一个自包含脚本:
        assembly = cq.Assembly(); assembly.add(...); assembly.constrain(...,'Axis'/'Point'/'Fixed');
        assembly.solve(); result = assembly.toCompound()
     零件全部以局部坐标加入, 位姿完全由约束求解器恢复;
  5. 在新进程中执行生成脚本, 用存储位姿核对求解结果 (座面圆心/法向残差), 写 assembly_constraints.json.
用法: conda run -n cadquery python -X utf8 exp_l_constraints.py <n_single> <n_two>
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, sys, glob, json, math, io, contextlib, subprocess
import numpy as np
import cadquery as cq
from OCP.gp import gp_Pnt, gp_Dir, gp_Trsf, gp_Vec, gp_Ax1

ROOT = _ROOT
CONV = os.path.join(ROOT, '1m_Convert')
sys.path.insert(0, CONV)
import fasteners as F

N_SINGLE = int(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 30
N_TWO = int(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 20
TOL_ST, TOL_TOUCH, TOL_POS, TOL_ANG = 1.0, 1.0, 1e-3, 0.05
SCRIPT_NAME = 'assembly_constrained_cadquery.py'
VERIFY = os.path.join(ROOT, '_review', 'verify_constrained_assembly.py')


# ----------------------------------------------------------------------------- geometry helpers
def place_trsf(axis, point, seat, flip):
    a, p, t = axis, point, seat
    final = gp_Trsf()
    anchor = (p[0] + a[0]*t, p[1] + a[1]*t, p[2] + a[2]*t)
    tT = gp_Trsf(); tT.SetTranslation(gp_Vec(*anchor)); final.Multiply(tT)
    dot = max(-1.0, min(1.0, a[2])); ang = math.acos(dot)
    if ang > 1e-4:
        rax = (-a[1], a[0], 0.0)
        if math.hypot(*rax) < 1e-9:
            rax = (1.0, 0.0, 0.0)
        tR = gp_Trsf(); tR.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(*rax)), ang); final.Multiply(tR)
    if flip:
        tF = gp_Trsf(); tF.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), math.pi); final.Multiply(tF)
    return final


def xf(c, T):
    P = gp_Pnt(*c).Transformed(T); return np.array([P.X(), P.Y(), P.Z()])


def unit(v):
    v = np.asarray(v, float); return v / (np.linalg.norm(v) + 1e-12)


def V(c):
    return np.array([c.x, c.y, c.z], float)


def unwrap(x):
    return x.val() if hasattr(x, 'val') else x


def planar(shape):
    return [f for f in shape.Faces() if f.geomType() == 'PLANE']


def normal(f):
    return unit(V(f.normalAt()))


def circles_on_axis(face, axis_pt, a, tol=2e-3):
    out = []
    for e in face.Edges():
        if e.geomType() != 'CIRCLE':
            continue
        c = V(e.Center()); d = c - axis_pt
        if np.linalg.norm(d - np.dot(d, a) * a) < tol:
            out.append(e)
    return sorted(out, key=lambda e: e.radius())


def local_face_for(placed_faces, local_faces, i, T):
    tgt = V(placed_faces[i].Center())
    for f in local_faces:
        if np.linalg.norm(xf(V(f.Center()), T) - tgt) < 1e-5:
            return f
    return None


def local_circle_for(local_face, placed_circle, T):
    tgt = V(placed_circle.Center())
    if placed_circle.ShapeType() == 'Vertex':        # 合成的轴线点 -> 反变换到局部坐标
        q = xf(tgt, T.Inverted())
        return cq.Vertex.makeVertex(float(q[0]), float(q[1]), float(q[2]))
    if placed_circle.geomType() == 'PLANE':
        return local_face if np.linalg.norm(xf(V(local_face.Center()), T) - tgt) < 1e-5 else None
    for e in local_face.Edges():
        if e.geomType() == 'CIRCLE' and np.linalg.norm(xf(V(e.Center()), T) - tgt) < 1e-5:
            return e
    return None


def key_of(sub):
    """局部子形状 -> 可序列化几何键 (生成脚本运行时据此重新定位该面/边)."""
    c = [round(float(x), 6) for x in V(sub.Center())]
    if sub.ShapeType() == 'Vertex':
        return dict(type='vertex', centre=c)
    if sub.geomType() == 'PLANE':
        n = [round(float(x), 6) for x in normal(sub)]
        return dict(type='face', centre=c, normal=n)
    return dict(type='circle', centre=c, radius=round(float(sub.radius()), 6))


def on_own_axis(w, oth, tol=1e-3):
    """合成点 w 是否落在对方零件自身的轴线上 (对方是本体 A/B 时恒真: 它们的转动已被固定)."""
    a_o, p_o = oth[4], oth[5]
    if a_o is None:
        return True
    d = np.asarray(w, float) - p_o
    return np.linalg.norm(d - np.dot(d, a_o) * a_o) < tol


def find_contact(placed, local, T_self, others, a, p, parallel=False):
    """parallel=False: 反法向相触的座面对 (Axis 180 + Point).
    parallel=True : 同向、共站 (<=1 mm)、同轴的面对 -- 压入式零件 (heat-set insert) 与孔口平齐/微凹, 无接触面 (Axis 0 + Point)."""
    pf, lf = planar(placed), planar(local)
    best = None
    for i, f in enumerate(pf):
        n = normal(f)
        if abs(abs(np.dot(n, a)) - 1) > 1e-3:
            continue
        cf = V(f.Center())
        seat_circ = circles_on_axis(f, p, a)
        if not seat_circ:
            dcf = cf - p
            if np.linalg.norm(dcf - np.dot(dcf, a) * a) < 1e-3:
                seat_circ = [f]
            else:                                            # 圆边被螺纹起始切成圆弧: 用座面站位处的轴线点
                w = p + a * float(np.dot(dcf, a))
                seat_circ = [cq.Vertex.makeVertex(float(w[0]), float(w[1]), float(w[2]))]
        for oth in others:
            name, o_local, o_placed, T_o = oth[:4]
            opf, olf = planar(o_placed), planar(o_local)
            for j, g in enumerate(opf):
                ng = normal(g)
                if abs(np.dot(n, ng) - (1 if parallel else -1)) > 1e-3:
                    continue
                if abs(np.dot(V(g.Center()) - cf, a)) > TOL_ST:
                    continue
                if parallel:
                    dist = abs(float(np.dot(V(g.Center()) - cf, a)))   # 同向面: 用站位差作为间隙
                else:
                    try:
                        dist = f.distance(g)
                    except Exception:
                        continue
                    if dist > TOL_TOUCH:
                        continue
                circ = circles_on_axis(g, p, a)
                if not circ:
                    stg = float(np.dot(V(g.Center()) - p, a))
                    for cyl in [x for x in o_placed.Faces() if x.geomType() == 'CYLINDER']:
                        for e in cyl.Edges():
                            if e.geomType() != 'CIRCLE' or not e.IsClosed():
                                continue
                            ce = V(e.Center()); d = ce - p
                            if np.linalg.norm(d - np.dot(d, a) * a) < 2e-3 and abs(np.dot(d, a) - stg) < 1e-3:
                                circ = [e]; break
                        if circ:
                            break
                if not circ:                                    # 圆边被拆成圆弧 -> 用对方面本身 (质心在轴上)
                    dg = V(g.Center()) - p
                    if np.linalg.norm(dg - np.dot(dg, a) * a) < 1e-3:
                        circ = [g]
                    else:
                        w = p + a * float(np.dot(dg, a))
                        circ = [cq.Vertex.makeVertex(float(w[0]), float(w[1]), float(w[2]))]
                if not circ or not seat_circ:
                    continue
                # 对方若是紧固件 (绕自身轴可自由转动), 配合点必须在其自身轴线上, 否则位姿不确定
                if not on_own_axis(V(circ[0].Center()), oth):
                    continue
                g_local = local_face_for(opf, olf, j, T_o)
                f_local = local_face_for(pf, lf, i, T_self)
                if g_local is None or f_local is None:
                    continue
                cl = local_circle_for(g_local, circ[0], T_o)
                if cl is None:
                    tgt = V(circ[0].Center())
                    for e in o_local.Edges():
                        if e.geomType() == 'CIRCLE' and np.linalg.norm(xf(V(e.Center()), T_o) - tgt) < 1e-5:
                            cl = e; break
                sl = local_circle_for(f_local, seat_circ[0], T_self)
                if cl is None or sl is None:
                    continue
                score = -dist * 1e6 + f.Area()
                if best is None or score > best[0]:
                    best = (score, f_local, f, name, cl, g_local, sl, seat_circ[0])
    return best


def find_datum(placed, local, T_self, others, a, p):
    """第三级回退 (压入件居中于壁厚、沉孔内的螺钉头等: 与任何面既不接触也不平齐):
    取本件最大的 ⟂轴 平面 f 与对方 (优先基体) 站位最近的 ⟂轴 平面 g 做 Axis 配合 (按存储相对朝向选 0/180),
    Point 配合取两件各自轴线上、f 站位处的基准点 (合成 Vertex). 位置完全由设计基准而非接触决定."""
    pf, lf = planar(placed), planar(local)
    cands = [(i, f) for i, f in enumerate(pf) if abs(abs(np.dot(normal(f), a)) - 1) < 1e-3]
    if not cands:
        return None
    i, f = max(cands, key=lambda t: t[1].Area())
    n = normal(f); cf = V(f.Center()); st_f = float(np.dot(cf - p, a))
    best = None
    for oth in others:
        name, o_local, o_placed, T_o = oth[:4]
        if oth[4] is not None:                              # 基准配合只挂到转动已固定的本体 A/B
            continue
        opf, olf = planar(o_placed), planar(o_local)
        for j, g in enumerate(opf):
            ng = normal(g)
            if abs(abs(np.dot(ng, a)) - 1) > 1e-3:
                continue
            gap = abs(float(np.dot(V(g.Center()) - cf, a)))
            pri = 0
            if best is None or (pri, gap) < (best[0], best[1]):
                best = (pri, gap, name, j, g, ng, opf, olf, T_o, o_local)
    if best is None:
        return None
    _, gap, name, j, g, ng, opf, olf, T_o, o_local = best
    f_local = local_face_for(pf, lf, i, T_self); g_local = local_face_for(opf, olf, j, T_o)
    if f_local is None or g_local is None:
        return None
    param = 0 if np.dot(n, ng) > 0 else None                  # None -> 默认 180 (反向)
    w = p + a * st_f
    wv = cq.Vertex.makeVertex(float(w[0]), float(w[1]), float(w[2]))
    sl = local_circle_for(f_local, wv, T_self); cl = local_circle_for(g_local, wv, T_o)
    return (0.0, f_local, f, name, cl, g_local, sl, wv), param


# ----------------------------------------------------------------------------- run original script
def run_script(path):
    rec, fcalls = [], []
    real_place, real_fastener = F.place, F.fastener

    def w_fastener(kind, *args):
        fcalls.append((kind, args))
        return real_fastener(kind, *args)

    def w_place(part, axis, point, seat, flip=False):
        placed = real_place(part, axis, point, seat, flip)
        rec.append(dict(local=unwrap(part), axis=tuple(axis), point=tuple(point), placed=placed,
                        trsf=place_trsf(tuple(axis), tuple(point), float(seat), bool(flip))))
        return placed
    F.place, F.fastener = w_place, w_fastener
    g = {'__name__': '__main__', '__file__': path}
    try:
        src = open(path, encoding='utf-8').read()
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, path, 'exec'), g)
    finally:
        F.place, F.fastener = real_place, real_fastener
    assert len(fcalls) == len(rec), 'fastener/place call mismatch'
    return g, rec, fcalls


# ----------------------------------------------------------------------------- script emission
HEADER = '''# Constraint-based CadQuery assembly, generated from assembly_cadquery.py by
# exp_l_constraints.py.  Unlike the original script, no part is positioned by an
# explicit rigid transform: every part is added to a cq.Assembly in its own local
# frame and its pose is recovered by mate constraints (Axis = antiparallel seating
# normals, Point = coincident circle centres) through assembly.solve().
import os, sys, math
_HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.insert(0, os.path.dirname(_HERE))
import cadquery as cq
from fasteners import fastener


def _load_part(_sub):
    _g = {'cq': cq, 'math': __import__('math'), '__name__': '_partexec'}
    exec(open(os.path.join(_HERE, _sub, 'cadquery.py'), encoding='utf-8').read(), _g)
    _r = _g.get('result')
    if _r is None:
        for _v in _g.values():
            if isinstance(_v, cq.Workplane): _r = _v
    return _r


def _shape(x):
    return x.val() if hasattr(x, 'val') else x


def _face(part, centre, normal, tol=1e-4):
    """Planar face of `part` (local frame) with the given centroid and normal."""
    for f in _shape(part).Faces():
        if f.geomType() != 'PLANE':
            continue
        c, n = f.Center(), f.normalAt()
        if math.dist((c.x, c.y, c.z), centre) < tol and n.x*normal[0] + n.y*normal[1] + n.z*normal[2] > 1 - 1e-6:
            return f
    raise RuntimeError('mate face not found: centre=%r normal=%r' % (centre, normal))


def _circle(part, centre, radius, tol=1e-4):
    """Circular edge of `part` (local frame) with the given centre and radius."""
    for e in _shape(part).Edges():
        if e.geomType() != 'CIRCLE' or abs(e.radius() - radius) > tol:
            continue
        c = e.Center()
        if math.dist((c.x, c.y, c.z), centre) < tol:
            return e
    raise RuntimeError('mate circle not found: centre=%r r=%r' % (centre, radius))


def _axis_point(centre):
    """Point on a part's hole/shank axis (local frame), used where the seating rim is
    split into arcs and therefore has no full circular edge to mate."""
    return cq.Vertex.makeVertex(*centre)


'''


def fmt_key(var, k):
    if k['type'] == 'vertex':
        return '_axis_point(%r)' % (tuple(k['centre']),)
    if k['type'] == 'face':
        return '_face(%s, %r, %r)' % (var, tuple(k['centre']), tuple(k['normal']))
    return '_circle(%s, %r, %r)' % (var, tuple(k['centre']), k['radius'])


def emit_script(adir, kind, fcalls, mates, part_names, fixed_rot=None):
    """mates: list of dict(part, other, kind, key_self, key_other)."""
    L = [HEADER]
    if kind == 'two':
        L.append("A = _load_part('partA')\nB = _load_part('partB')\n")
    else:
        L.append("A = _load_part('part')\n")
    L.append("assembly = cq.Assembly(name=%r)\n" % os.path.basename(adir))
    L.append("assembly.add(A, name='A')\nassembly.constrain('A', 'Fixed')\n")
    if kind == 'two':
        L.append("assembly.add(B, name='B')\n")
        if fixed_rot and 'B' in fixed_rot:
            L.append("# single-fastener joint: rotation about the common axis is a free degree of freedom (Sec. 4.8);\n"
                     "# it is fixed to the stored value, as in the explicit-pose script\n"
                     "assembly.constrain('B', 'FixedRotation', param=%r)\n" % (fixed_rot['B'],))
    for k, (fk, fargs) in enumerate(fcalls):
        L.append("f%d = fastener(%s)\nassembly.add(f%d, name='f%d')\n" % (k, ', '.join(repr(x) for x in (fk,) + tuple(fargs)), k, k))
    L.append('\n# mate constraints: per part an Axis mate (default param 180 = antiparallel seating normals;\n'
             '# param=0 = flush/recessed press-fit part with same-direction normals) plus a Point mate (coincident centres)\n')
    for m in mates:
        extra = ', param=%r' % m['param'] if m.get('param') is not None else ''
        if m.get('cls') == 'datum' and m['kind'] == 'Axis':
            L.append("# %s: press-fit / counterbored part without a seating contact -- located by design datum "
                     "(axis point at its station), not by a touching face\n" % m['part'])
        L.append("assembly.constrain(%r, %s, %r, %s, %r%s)\n" % (
            m['part'], fmt_key(m['part'], m['key_self']), m['other'], fmt_key(m['other'], m['key_other']), m['kind'], extra))
    L.append('\nassembly.solve()\nresult = assembly.toCompound()\n')
    path = os.path.join(adir, SCRIPT_NAME)
    open(path, 'w', encoding='utf-8', newline='\n').write(''.join(L))
    return path


# ----------------------------------------------------------------------------- per assembly
def convert(adir, kind):
    g, rec, fcalls = run_script(os.path.join(adir, 'assembly_cadquery.py'))
    parts = g['parts']
    A = unwrap(parts[0])
    I = gp_Trsf()
    others = [('A', A, A, I, None, None)]
    mates, check = [], {}
    order = []
    fixed_rot = {}
    if kind == 'two':
        B_local = unwrap(g['_load_part']('partB')); B_placed = unwrap(parts[1])
        order.append(('B', B_local, B_placed, unit(rec[0]['axis']), np.array(rec[0]['point'], float), g['_t']))
        # 单孔连接绕轴转动自由 (见正文): 用存储位姿的欧拉角固定 B 的转动, 与原脚本"由变换数值固定"等价
        from OCP.gp import gp_Extrinsic_XYZ
        e = g['_t'].GetRotation().GetEulerAngles(gp_Extrinsic_XYZ)
        fixed_rot['B'] = tuple(round(math.degrees(x), 9) for x in e)
    for k, r in enumerate(rec):
        order.append(('f%d' % k, r['local'], r['placed'], unit(r['axis']), np.array(r['point'], float), r['trsf']))
    for name, local, placed, a, p, T_self in order:
        ct = find_contact(placed, local, T_self, others, a, p)
        axis_param = None
        if ct is None:
            ct = find_contact(placed, local, T_self, others, a, p, parallel=True)
            axis_param = 0
        mate_class = 'contact' if ct is not None and axis_param is None else 'flush'
        if ct is None:
            fd = find_datum(placed, local, T_self, others, a, p)
            if fd is None:
                return dict(dir=os.path.basename(adir), kind=kind, ok=False, why='no contact pair for %s' % name)
            ct, axis_param = fd; mate_class = 'datum'
        _, seat_local, seat_placed, other, circ_local, other_local_face, seat_circ_local, seat_circ_placed = ct
        mates.append(dict(part=name, other=other, kind='Axis', param=axis_param, cls=mate_class, key_self=key_of(seat_local), key_other=key_of(other_local_face)))
        mates.append(dict(part=name, other=other, kind='Point', cls=mate_class, key_self=key_of(seat_circ_local), key_other=key_of(circ_local)))
        # 存储位姿下的核对量: 该零件 Point 配合子形状的世界圆心 + 座面世界法向
        check[name] = dict(key=key_of(seat_circ_local), face_key=key_of(seat_local),
                           centre=[round(float(x), 6) for x in V(seat_circ_placed.Center())],
                           face_centre=[round(float(x), 6) for x in V(seat_placed.Center())],
                           normal=[round(float(x), 6) for x in normal(seat_placed)])
        others.append((name, local, placed, T_self, None if name == 'B' else a, None if name == 'B' else p))
    spath = emit_script(adir, kind, fcalls, mates, [o[0] for o in order], fixed_rot)
    n_solids_ref = sum(len(unwrap(q).Solids()) for q in parts if q is not None)   # 轴承等多实体件按实体计
    json.dump(dict(script=SCRIPT_NAME, kind=kind, n_parts=1 + len(order), n_solids=n_solids_ref, mates=mates, stored_pose_check=check),
              open(os.path.join(adir, 'assembly_constraints.json'), 'w'), indent=1)
    return dict(dir=os.path.basename(adir), kind=kind, ok=True, n_mates=len(mates), script=spath,
                n_axis0=sum(1 for m in mates if m.get('param') == 0),
                n_datum=sum(1 for m in mates if m.get('cls') == 'datum' and m['kind'] == 'Axis'),
                n_flush=sum(1 for m in mates if m.get('cls') == 'flush' and m['kind'] == 'Axis'),
                n_contact=sum(1 for m in mates if m.get('cls') == 'contact' and m['kind'] == 'Axis'),
                n_vertex=sum(1 for m in mates if 'vertex' in (m['key_self']['type'], m['key_other']['type'])))


def verify_chunk(recs):
    """在新解释器中运行一批生成脚本并回填验证结果 (失败的脚本删除)."""
    emitted = [r for r in recs if r.get('ok')]
    if not emitted:
        return
    try:
        ver = subprocess.run([sys.executable, '-X', 'utf8', VERIFY] + [r['script'] for r in emitted],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=1800)
        lines = ver.stdout.splitlines()
    except subprocess.TimeoutExpired as e:
        lines = (e.stdout or b'').decode('utf-8', 'ignore').splitlines() if isinstance(e.stdout, bytes) else (e.stdout or '').splitlines()
    vres = {}
    for line in lines:
        if line.startswith('{'):
            d = json.loads(line); vres[d['script']] = d
    for r in emitted:
        v = vres.get(r['script'])
        if v is None:
            r.update(ok=False, why='verification produced no result')
            if os.path.exists(r['script']):
                os.remove(r['script'])
            continue
        r.update(ok=bool(v['ok']), max_pos=v['max_pos'], max_ang=v['max_ang'], gaps=v['gaps'], why=v.get('why'))
        jp = os.path.join(os.path.dirname(r['script']), 'assembly_constraints.json')
        dd = json.load(open(jp)); dd.update(solved=bool(v['ok']), max_pos_residual_mm=v['max_pos'], max_axis_residual_deg=v['max_ang'])
        json.dump(dd, open(jp, 'w'), indent=1)
        if not v['ok'] and os.path.exists(r['script']):
            os.remove(r['script'])
        print('verify', r['dir'][:24], v['ok'], v['max_pos'], v['max_ang'], flush=True)


def summarise(out, n_single, n_two):
    ok = [r for r in out if r.get('ok')]
    return dict(n=len(out), n_ok=len(ok),
                single_ok='%d/%d' % (sum(1 for r in ok if r['kind'] == 'single'), n_single),
                two_ok='%d/%d' % (sum(1 for r in ok if r['kind'] == 'two'), n_two),
                max_pos_residual_mm=max([r['max_pos'] for r in ok], default=None),
                max_axis_residual_deg=max([r['max_ang'] for r in ok], default=None),
                mates_total=sum(r.get('n_mates', 0) for r in ok),
                mates_axis_parallel=sum(r.get('n_axis0', 0) for r in ok),
                mates_vertex=sum(r.get('n_vertex', 0) for r in ok),
                parts_contact=sum(r.get('n_contact', 0) for r in ok),
                parts_flush=sum(r.get('n_flush', 0) for r in ok),
                parts_datum=sum(r.get('n_datum', 0) for r in ok),
                parts_exact=sum(1 for r in ok for gp in r['gaps'] if gp < 1e-3),
                parts_total=sum(len(r['gaps']) for r in ok),
                corrected_gaps_mm=sorted(set(gp for r in ok for gp in r['gaps'] if gp >= 1e-3))[:12],
                failures=[(r['dir'][:20], r.get('why'), r.get('max_pos')) for r in out if not r.get('ok')])


def main():
    """用法: exp_l_constraints.py <n_single> <n_two> [--resume]  (n=-1 表示全部). 分块转换+验证, 每块后落盘, 可断点续跑."""
    resume = '--resume' in sys.argv
    singles = sorted(glob.glob(os.path.join(CONV, 'assemblies_slim', '*__asm')))
    twos = sorted(glob.glob(os.path.join(CONV, 'two_part_assemblies_slim', '*__two')))
    if N_SINGLE >= 0:
        singles = singles[:N_SINGLE]
    if N_TWO >= 0:
        twos = twos[:N_TWO]
    shard = [a for a in sys.argv if a.startswith('--shard=')]
    k_sh, n_sh = (int(x) for x in shard[0].split('=')[1].split('/')) if shard else (0, 1)
    outp = os.path.join(ROOT, '_review', 'exp_l_constraints.json' if n_sh == 1 else 'exp_l_constraints_shard%d.json' % k_sh)
    done = {}
    if resume:
        for f in glob.glob(os.path.join(ROOT, '_review', 'exp_l_constraints*.json')):
            if 'sample50' in f:
                continue
            try:
                for r in json.load(open(f))['records']:
                    done[r['dir']] = r
            except Exception:
                pass
    out = []
    todo = [(k, d) for k, lst in (('single', singles), ('two', twos)) for d in lst][k_sh::n_sh]
    CH = 20
    for c0 in range(0, len(todo), CH):
        chunk = todo[c0:c0 + CH]
        recs = []
        for kind, d in chunk:
            name = os.path.basename(d)
            if name in done and done[name].get('ok') and os.path.exists(os.path.join(d, SCRIPT_NAME)):
                out.append(done[name]); continue
            old = os.path.join(d, SCRIPT_NAME)
            if os.path.exists(old):
                os.remove(old)
            try:
                r = convert(d, kind)
            except Exception as e:
                r = dict(dir=name, kind=kind, ok=False, why='%s: %s' % (type(e).__name__, str(e)[:80]))
            print(r, flush=True); recs.append(r)
        verify_chunk(recs)
        out.extend(recs)
        summ = summarise(out, len(singles), len(twos))
        json.dump(dict(summary=summ, records=out), open(outp, 'w'), indent=1)
        print('--- progress %d/%d  ok=%d' % (len(out), len(todo), summ['n_ok']), flush=True)
    print(json.dumps(summarise(out, len(singles), len(twos)), indent=1))


if __name__ == '__main__':
    main()
