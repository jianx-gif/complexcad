# -*- coding: utf-8 -*-
"""实验CC: 参数级去重 (批注 p53 #181): 测试集 400 件与训练集之间, 是否存在
  (a) 源代码去掉注释与空白后完全相同的程序 (代码级重复);
  (b) 具名参数值多重集 + 操作多重集完全相同的程序 (参数级重复: 同一模板同一组数);
  (c) 只有操作多重集相同、参数值不同 (同一模板换参数, 统计每件测试模型的同模板训练件数).
用法: python exp_cc_param_dedup.py
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, re, json, collections, hashlib

R = _ROOT
PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)


def load(f):
    return [l.strip() for l in open(os.path.join(R, 'splits', f), encoding='utf-8') if l.strip()]


test, train = load('test_400.txt'), load('train.txt')
ops = {}
for l in open(os.path.join(R, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8'):
    j = json.loads(l)
    ops[j['uuid']] = tuple(sorted(o.lower() for o in (j.get('ops') or [])))


def keys(u):
    src = open(os.path.join(R, 'output', u, 'cadquery.py'), encoding='utf-8', errors='replace').read()
    code = re.sub(r'#.*', '', src)
    code = re.sub(r'\s+', '', code)
    vals = tuple(sorted(round(float(v), 6) for _, v in PARAM_RE.findall(src)))
    return hashlib.sha1(code.encode()).hexdigest(), (vals, ops[u]), ops[u]


tr_code, tr_param, tr_ops = collections.Counter(), collections.Counter(), collections.Counter()
for u in train:
    c, p, o = keys(u)
    tr_code[c] += 1; tr_param[p] += 1; tr_ops[o] += 1
dup_code = dup_param = 0
same_template = []
for u in test:
    c, p, o = keys(u)
    dup_code += tr_code[c] > 0
    dup_param += tr_param[p] > 0 and len(p[0]) > 0
    same_template.append(tr_ops[o])
same_template.sort()
out = dict(n_test=len(test), n_train=len(train),
           test_with_code_duplicate_in_train=dup_code,
           test_with_parameter_and_operation_duplicate_in_train=dup_param,
           train_models_with_same_operation_multiset_per_test_model=dict(
               median=same_template[len(same_template) // 2], zero=sum(1 for x in same_template if x == 0),
               max=same_template[-1]))
json.dump(out, open(os.path.join(R, '_review', 'exp_cc_param_dedup.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
