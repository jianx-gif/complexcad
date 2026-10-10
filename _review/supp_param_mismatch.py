# -*- coding: utf-8 -*-
"""Classify the description parameter values that exp_c_text_audit cannot match:
   (a) name not resolvable by the independent evaluator (module-level assignment / keyword default / arithmetic)
   (b) resolvable but different value
Same evaluator as exp_c_text_audit.py. Usage (cadfit-env): python -X utf8 supp_param_mismatch.py"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import json, re, glob, os, collections, ast, math as _math

ROOT = _ROOT
PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)


def source_params(src):
    params_src = {m[0]: float(m[1]) for m in PARAM_RE.findall(src)}
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
    for m in re.finditer(r"([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*[,)]", src):
        params_src.setdefault(m.group(1), float(m.group(2)))
    return params_src


tot = collections.Counter(); ex_unres = []; ex_diff = []
for d in sorted(glob.glob(os.path.join(ROOT, 'output', '*'))):
    dj = os.path.join(d, 'description.json'); py = os.path.join(d, 'cadquery.py')
    if not (os.path.isfile(dj) and os.path.isfile(py)):
        continue
    desc = json.load(open(dj, encoding='utf-8'))
    src = open(py, encoding='utf-8', errors='replace').read()
    ps = source_params(src)
    for k, v in (desc.get('parameters') or {}).items():
        if not isinstance(v, (int, float)):
            tot['non_numeric'] += 1
            continue
        tot['checked'] += 1
        if k in ps and abs(ps[k] - float(v)) < 1e-9:
            tot['exact'] += 1
        elif k not in ps:
            tot['unresolvable'] += 1
            # is the name assigned anywhere in the source (e.g. inside a function / loop / tuple)?
            if re.search(r'\b%s\s*=' % re.escape(k), src):
                tot['unresolvable_but_assigned_in_source'] += 1
            if len(ex_unres) < 12:
                ex_unres.append((os.path.basename(d)[:8], k, v))
        else:
            tot['different_value'] += 1
            if len(ex_diff) < 12:
                ex_diff.append((os.path.basename(d)[:8], k, v, ps[k]))
print(json.dumps(tot, indent=1))
print('unresolvable examples:', ex_unres)
print('different-value examples:', ex_diff)
json.dump({'counts': tot, 'unresolvable_examples': ex_unres, 'different_value_examples': ex_diff},
          open(os.path.join(ROOT, '_review', 'supp_param_mismatch.json'), 'w'), indent=1)
