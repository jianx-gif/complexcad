# -*- coding: utf-8 -*-
"""实验FF: 按"操作"而非按名字关键词统计参数取值 (批注 #227/#229).
从 metadata.json 的 cadquery_ops_json 取每次调用的实参 (变量名 / 数字字面量 / 表达式),
用源程序的模块级赋值与表达式求值解析成数值, 按 (操作, 实参角色) 汇总 n、最小、P5、中位、P95、最大.
角色: chamfer/fillet 第1参(距离/半径); revolve 第1参(角度, 省略=360); hole/cboreHole/cskHole 第1参(直径)、第2参(深度, 可省略);
      extrude/cutBlind 第1参(距离); shell 第1参(壁厚).  loft/sweep 没有标量实参, 只计次数.
用法: python exp_ff_param_by_operation.py
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, re, json, ast, math, glob, collections
import numpy as np

R = _ROOT
PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)
ROLES = {'chamfer': [(0, 'distance')], 'fillet': [(0, 'radius')], 'revolve': [(0, 'angle (deg)')],
         'hole': [(0, 'diameter'), (1, 'depth')], 'cboreHole': [(0, 'diameter')], 'cskHole': [(0, 'diameter')],
         'extrude': [(0, 'distance')], 'cutBlind': [(0, 'depth')], 'shell': [(0, 'thickness')]}


def env_of(src):
    env = {n: float(v) for n, v in PARAM_RE.findall(src)}
    try:
        for node in ast.parse(src).body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                nm = node.targets[0].id
                if nm in env:
                    continue
                try:
                    v = eval(compile(ast.Expression(node.value), '<p>', 'eval'),
                             {'__builtins__': {}, 'math': math, 'min': min, 'max': max, 'abs': abs,
                              'int': int, 'float': float, 'round': round}, dict(env))
                    if isinstance(v, (int, float)):
                        env[nm] = float(v)
                except Exception:
                    pass
    except Exception:
        pass
    return env


def resolve(arg, env):
    a = str(arg).strip()
    if re.match(r'^-?\d+(\.\d+)?$', a):
        return float(a)
    if re.match(r'^[A-Za-z_]\w*$', a):
        return env.get(a)
    m = re.match(r"^Name\(id='(\w+)'", a)
    if m:
        return env.get(m.group(1))
    try:
        v = eval(a, {'__builtins__': {}, 'math': math}, dict(env))
        return float(v) if isinstance(v, (int, float)) else None
    except Exception:
        return None


vals = collections.defaultdict(list); unresolved = collections.Counter(); calls = collections.Counter()
for d in glob.glob(os.path.join(R, 'output', '*')):
    mp, py = os.path.join(d, 'metadata.json'), os.path.join(d, 'cadquery.py')
    if not (os.path.isfile(mp) and os.path.isfile(py)):
        continue
    ops = json.load(open(mp, encoding='utf-8')).get('cadquery_ops_json') or []
    if isinstance(ops, str):
        ops = json.loads(ops)
    env = env_of(open(py, encoding='utf-8', errors='replace').read())
    for o in ops:
        name = o.get('op_name')
        if name in ('loft', 'sweep'):
            calls[name] += 1
        if name not in ROLES:
            continue
        calls[name] += 1
        args = o.get('args') or []
        for idx, role in ROLES[name]:
            if idx >= len(args):
                if name == 'revolve' and idx == 0:
                    vals[(name, role)].append(360.0)
                continue
            v = resolve(args[idx], env)
            if v is None:
                unresolved[(name, role)] += 1
            else:
                vals[(name, role)].append(v)
rows = []
for (op, role), v in sorted(vals.items()):
    a = np.array(v)
    rows.append(dict(operation=op, role=role, n=len(a), unresolved=unresolved[(op, role)],
                     min=round(float(a.min()), 3), p5=round(float(np.quantile(a, .05)), 3),
                     median=round(float(np.median(a)), 3), p95=round(float(np.quantile(a, .95)), 3),
                     max=round(float(a.max()), 3), nonpositive=int((a <= 0).sum())))
res = dict(rows=rows, calls=dict(calls))
json.dump(res, open(os.path.join(R, '_review', 'exp_ff_param_by_operation.json'), 'w'), indent=1)
for r in rows:
    print(r)
print('calls', dict(calls))
