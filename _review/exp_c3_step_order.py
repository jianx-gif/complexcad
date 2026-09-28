# -*- coding: utf-8 -*-
"""实验C3: 文本描述「建模步骤顺序」自动检查 (导师 2026-09-28 反馈: 194/200 步骤顺序被人工否决).

独立于生成器和上游 ops 日志: 用 Python ast 重新解析 cadquery.py, 取所有属性调用
(.extrude/.hole/.fillet/...) 中属于三维建模操作的调用, 按源码位置 (lineno, col_offset)
排序 —— 直线脚本的执行顺序 —— 得到「参考步骤序列」; 与 description.json 的
operation_sequence 逐项比较:
  * exact: 序列完全一致 (同操作、同顺序、同次数)
  * order_ok: 忽略次数, 去重后的相对顺序一致 (子序列)
  * has_sketch_primitive: 描述步骤里仍含 circle/rect/polygon/polyline
另外对人工审查的 200 件样本 (_review/text_audit/checklist.csv) 单独汇总.
用法 (cadfit-env): python -X utf8 exp_c3_step_order.py [output_dir]
"""
import ast, csv, json, os, sys, collections

ROOT = r'E:/3005/data'
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'output')
OPS3D = {"extrude", "cut", "hole", "cboreHole", "cskHole", "fillet", "chamfer",
         "revolve", "sweep", "loft", "union", "intersect", "shell", "box",
         "cutBlind", "cutThruAll", "twistExtrude", "mirror"}
SKETCH = {"circle", "rect", "polygon", "polyline"}


def reference_sequence(src):
    tree = ast.parse(src)
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr in OPS3D:
            # END position of the call = its closing parenthesis: in a chained
            # expression the inner call closes first, so end positions give the
            # execution order (independent of the upstream ops log).
            calls.append((node.end_lineno, node.end_col_offset, node.func.attr))
    calls.sort()
    return [c[2] for c in calls]


def subseq(a, b):
    """a is a subsequence of b (order preserved)."""
    it = iter(b)
    return all(x in it for x in a)


def main():
    sample = set()
    ck = os.path.join(ROOT, '_review', 'text_audit', 'checklist.csv')
    if os.path.isfile(ck):
        sample = {r['uuid'] for r in csv.DictReader(open(ck, encoding='utf-8'))}
    tot = collections.Counter(); smp = collections.Counter()
    bad = []
    for u in sorted(os.listdir(OUT)):
        dj = os.path.join(OUT, u, 'description.json'); py = os.path.join(OUT, u, 'cadquery.py')
        if not (os.path.isfile(dj) and os.path.isfile(py)):
            continue
        desc = json.load(open(dj, encoding='utf-8'))
        seq = list(desc.get('operation_sequence') or [])
        try:
            ref = reference_sequence(open(py, encoding='utf-8', errors='replace').read())
        except SyntaxError:
            tot['unparsable'] += 1
            continue
        exact = seq == ref
        dedup = lambda s: [x for i, x in enumerate(s) if x not in s[:i]]
        order_ok = dedup(seq) == dedup(ref)
        sk = any(s in SKETCH for s in seq)
        for c, flag in ((tot, True), (smp, u in sample)):
            if not flag:
                continue
            c['n'] += 1; c['exact'] += exact; c['order_ok'] += order_ok
            c['has_sketch_primitive'] += sk; c['same_multiset'] += (sorted(seq) == sorted(ref))
        if not exact and len(bad) < 8:
            bad.append((u[:8], seq, ref))
    res = {'n_models': tot['n'], 'exact_sequence': tot['exact'], 'exact_rate': round(tot['exact'] / max(1, tot['n']), 4),
           'order_ok_dedup': tot['order_ok'], 'order_ok_rate': round(tot['order_ok'] / max(1, tot['n']), 4),
           'same_multiset': tot['same_multiset'], 'with_sketch_primitive': tot['has_sketch_primitive'],
           'unparsable': tot['unparsable'],
           'sample200': {'n': smp['n'], 'exact': smp['exact'], 'order_ok_dedup': smp['order_ok'],
                         'with_sketch_primitive': smp['has_sketch_primitive'], 'same_multiset': smp['same_multiset']},
           'examples_not_exact': bad}
    print(json.dumps(res, indent=1))
    json.dump(res, open(os.path.join(ROOT, '_review', 'exp_c3_step_order.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
