# -*- coding: utf-8 -*-
"""实验C: 文本描述自动一致性质检 (批注p27), 全量9980.
独立于生成器: 用正则直接扫 cadquery.py 源码得到操作集合, 与 description.json 对照;
参数值与源码模块级赋值对照."""
import json, re, glob, os, collections

ROOT = r'E:/3005/data'
# 3D modelling operations only: 2D sketch primitives (rect, circle, polygon, polyline,
# ellipse, slot2D, offset2D, text) define a profile and are no longer listed as steps
# (generator fix of 2026-09-28 after the human review; see exp_c3_step_order.py).
OP_RE = re.compile(r"\.(revolve|sweep|loft|fillet|chamfer|extrude|shell|cutBlind|cutThruAll|hole|cboreHole|cskHole|union|cut|intersect|box|mirror|twistExtrude)\(", re.I)
PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)

n = miss_op = extra_op = 0
val_total = val_ok = 0
op_prec_n = op_prec_d = op_rec_n = op_rec_d = 0
bad_examples = []
for d in glob.glob(os.path.join(ROOT, 'output', '*')):
    dj = os.path.join(d, 'description.json')
    py = os.path.join(d, 'cadquery.py')
    if not (os.path.isfile(dj) and os.path.isfile(py)):
        continue
    n += 1
    desc = json.load(open(dj, encoding='utf-8'))
    src = open(py, encoding='utf-8', errors='replace').read()
    # 独立解析的操作multiset
    ind = collections.Counter(m.lower() for m in OP_RE.findall(src))
    ind_set = set(ind)
    txt_set = set(k.lower() for k in (desc.get('operation_counts') or {}))
    # 文本precision: 文本声称的操作有多少在独立解析中存在
    op_prec_n += len(txt_set & ind_set); op_prec_d += len(txt_set)
    # 文本recall: 独立解析出的操作有多少被文本覆盖
    op_rec_n += len(ind_set & txt_set); op_rec_d += len(ind_set)
    if txt_set - ind_set:
        extra_op += 1
        if len(bad_examples) < 5:
            bad_examples.append((os.path.basename(d), 'extra', sorted(txt_set - ind_set)))
    if ind_set - txt_set:
        miss_op += 1
    # 参数值对照: description.parameters 的每个值应等于源码同名赋值
    params_src = {m[0]: float(m[1]) for m in PARAM_RE.findall(src)}
    # 表达式赋值求值(仅算术+已知名), 覆盖 a = b * 2 之类
    import ast, math as _math
    try:
        tree = ast.parse(src)
        env = dict(params_src)
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                nm = node.targets[0].id
                if nm in env:
                    continue
                try:
                    code = compile(ast.Expression(node.value), '<p>', 'eval')
                    v = eval(code, {'__builtins__': {}, 'math': _math, 'min': min, 'max': max, 'abs': abs, 'int': int, 'float': float, 'round': round}, dict(env))
                    if isinstance(v, (int, float)):
                        env[nm] = float(v)
                except Exception:
                    pass
        params_src = env
    except Exception:
        pass
    # 关键字参数形式: SimpleNamespace(inner_radius=30.0,...) / 函数默认值
    for m in re.finditer(r"([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*[,)]", src):
        params_src.setdefault(m.group(1), float(m.group(2)))
    for k, v in (desc.get('parameters') or {}).items():
        if not isinstance(v, (int, float)):
            continue
        val_total += 1
        if k in params_src and abs(params_src[k] - float(v)) < 1e-9:
            val_ok += 1

out = {
    'n_models': n,
    'op_precision': round(op_prec_n / max(1, op_prec_d), 4),
    'op_recall': round(op_rec_n / max(1, op_rec_d), 4),
    'models_with_extra_claimed_op': extra_op,
    'models_with_missed_op': miss_op,
    'param_values_checked': val_total,
    'param_values_exact': val_ok,
    'param_value_accuracy': round(val_ok / max(1, val_total), 4),
}
print(json.dumps(out, indent=1))
print('extra examples:', bad_examples)
json.dump(out, open(os.path.join(ROOT, '_review', 'exp_c_text_audit.json'), 'w'), indent=1)
