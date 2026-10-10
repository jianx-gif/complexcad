# -*- coding: utf-8 -*-
"""实验BB: 闭环改善是否显著 (导师第5条: "证明复杂操作识别率、参数误差或工程可编辑性显著改善").

同一 400 件测试集上, 按模型配对比较各训练臂 (与 exp_j 同一解析器 parse_ops):
  1. code-level macro-F1 (五个复杂操作) 的差值: 配对 bootstrap (10000 次重采 400 件模型), 95% CI 与单侧 p
  2. 每件含复杂操作的模型"至少识别出一个真值复杂操作": McNemar 精确检验 (二项)
  3. 严格 macro-F1 (不可执行的程序记为全未识别): 同样的 bootstrap
  4. 可编辑性: 具名参数占比 (exp_q) 与编辑测试 (exp_s) 直接引用, Fisher 精确检验对比 0 %
比较对: ComplexCAD vs 对照; ComplexCAD vs 原版(同 mm/100 输入); +文本 vs ComplexCAD; +图纸 vs ComplexCAD.
用法 (cadfit-env): python exp_bb_loop_significance.py
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, sys, json, random, math

ROOT = _ROOT
sys.path.insert(0, os.path.join(ROOT, '1m_Convert', 'koor'))
from eval_predictions import parse_ops

OPS = ['loft', 'revolve', 'sweep', 'chamfer', 'fillet']
ARMS = ['cadrille_scale100', 'cadrille_ctrl', 'cadrille_cc', 'cadrille_cc_text', 'cadrille_cc_draw', 'cadrille_cc_r2', 'cadrille_cc_run1_reinfer', 'cadrille_cc_draw_qvu010']
gt = {}
for line in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8'):
    j = json.loads(line)
    gt[j['uuid']] = set(o.lower() for o in (j.get('ops') or []))
test = [l.strip() for l in open(os.path.join(ROOT, 'predictions', 'test_subset.txt'), encoding='utf-8') if l.strip()]
valid = {}
for a in ARMS:
    valid[a] = {json.loads(l)['uuid']: bool(json.loads(l).get('valid'))
                for l in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'pred_metrics_%s.jsonl' % a), encoding='utf-8') if l.strip()}

pred = {a: {} for a in ARMS}
for a in ARMS:
    for u in test:
        p = os.path.join(ROOT, 'predictions', a, u + '.py')
        try:
            pred[a][u] = set(o.lower() for o in parse_ops(open(p, encoding='utf-8', errors='replace').read()))
        except Exception:
            pred[a][u] = set()
units = [u for u in test if u in gt]


def macro_f1(arm, idx, strict=False):
    f1s = []
    for o in OPS:
        tp = fp = fn = 0
        for u in idx:
            g = o in gt[u]
            p = o in pred[arm][u] and (valid[arm].get(u, False) if strict else True)
            if g and p: tp += 1
            elif p: fp += 1
            elif g: fn += 1
        P = tp / max(1, tp + fp); R = tp / max(1, tp + fn)
        f1s.append(2 * P * R / max(1e-9, P + R))
    return sum(f1s) / len(f1s)


def boot(a, b, strict=False, B=10000):
    random.seed(0)
    base = macro_f1(a, units, strict) - macro_f1(b, units, strict)
    diffs = []
    n = len(units)
    for _ in range(B):
        idx = [units[random.randrange(n)] for _ in range(n)]
        diffs.append(macro_f1(a, idx, strict) - macro_f1(b, idx, strict))
    diffs.sort()
    lo, hi = diffs[int(0.025 * B)], diffs[int(0.975 * B)]
    p_one = sum(1 for d in diffs if d <= 0) / B
    return round(base, 3), round(lo, 3), round(hi, 3), p_one


def mcnemar(a, b):
    """units with >=1 GT complex op: does the arm name at least one of them?"""
    cx = [u for u in units if gt[u] & set(OPS)]
    hit = lambda arm, u: bool(pred[arm][u] & gt[u] & set(OPS))
    b01 = sum(1 for u in cx if not hit(a, u) and hit(b, u))
    b10 = sum(1 for u in cx if hit(a, u) and not hit(b, u))
    n = b01 + b10
    # exact two-sided binomial test on the discordant pairs
    k = min(b01, b10)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n * 2 if n else 1.0
    return dict(n_complex=len(cx), a_hits=sum(hit(a, u) for u in cx), b_hits=sum(hit(b, u) for u in cx),
                discordant_a_only=b10, discordant_b_only=b01, p_two_sided=min(1.0, p))


out = {}
for a, b in (('cadrille_cc', 'cadrille_ctrl'), ('cadrille_cc', 'cadrille_scale100'),
             ('cadrille_cc_text', 'cadrille_cc'), ('cadrille_cc_draw', 'cadrille_cc'), ('cadrille_cc_draw_qvu010', 'cadrille_cc'), ('cadrille_cc_draw_qvu010', 'cadrille_cc_draw'),
             ('cadrille_cc_r2', 'cadrille_ctrl'), ('cadrille_cc_run1_reinfer', 'cadrille_ctrl'),
             ('cadrille_cc', 'cadrille_cc_r2'), ('cadrille_cc_run1_reinfer', 'cadrille_cc')):
    key = '%s_vs_%s' % (a, b)
    out[key] = dict(macroF1_code=boot(a, b), macroF1_strict=boot(a, b, strict=True), mcnemar=mcnemar(a, b))
    print(key, json.dumps(out[key]))
json.dump(out, open(os.path.join(ROOT, '_review', 'exp_bb_loop_significance.json'), 'w'), indent=1)
