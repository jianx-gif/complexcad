# -*- coding: utf-8 -*-
"""实验J: 五复杂操作 per-op precision/recall/F1 (批注p55).
GT: metrics.jsonl ops; 预测: 复用 eval_predictions.parse_ops 解析各方法预测代码.
"""
import os, sys, json

ROOT = r'E:/3005/data'
sys.path.insert(0, os.path.join(ROOT, '1m_Convert', 'koor'))
from eval_predictions import parse_ops

OPS = ['loft', 'revolve', 'sweep', 'chamfer', 'fillet']
METHODS = ['cadrecode', 'cadrille', 'retrieval', 'zero2cad', 'cadfit',
           'cadrille_pc_text', 'cadrille_img_text', 'cadrille_ft',
           'cadrille_cc', 'cadrille_ctrl', 'cadrille_scale100', 'cadrille_cc_text', 'cadrille_cc_draw', 'cadrille_cc_draw_qvu010',
           'cadrille_cc_r2', 'cadrille_cc_run1_reinfer', 'retrieval_dedup']      # 闭环: 微调 / 对照 / 基线 (/100 输入)

gt = {}
for line in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8'):
    j = json.loads(line)
    gt[j['uuid']] = set(o.lower() for o in (j.get('ops') or []))

test = [l.strip() for l in open(os.path.join(ROOT, 'predictions', 'test_subset.txt'), encoding='utf-8') if l.strip()]

out = {}
for m in METHODS:
    pdir = os.path.join(ROOT, 'predictions', m)
    if not os.path.isdir(pdir):
        continue
    res = {}
    tp = {o: 0 for o in OPS}; fp = {o: 0 for o in OPS}; fn = {o: 0 for o in OPS}
    n = 0
    for u in test:
        pp = os.path.join(pdir, u + '.py')
        if not os.path.isfile(pp) or u not in gt:
            continue
        n += 1
        try:
            code = open(pp, encoding='utf-8', errors='replace').read()
            pred = set(o.lower() for o in parse_ops(code))
        except Exception:
            pred = set()
        for o in OPS:
            g, p = o in gt[u], o in pred
            if g and p: tp[o] += 1
            elif p and not g: fp[o] += 1
            elif g and not p: fn[o] += 1
    f1s = []
    for o in OPS:
        P = tp[o] / max(1, tp[o] + fp[o])
        R = tp[o] / max(1, tp[o] + fn[o])
        F = 2 * P * R / max(1e-9, P + R)
        res[o] = {'P': round(P, 3), 'R': round(R, 3), 'F1': round(F, 3),
                  'support': tp[o] + fn[o]}
        f1s.append(F)
    res['macro_F1'] = round(sum(f1s) / len(f1s), 3)
    res['n'] = n
    out[m] = res
    print(m, 'n=%d' % n, 'macroF1=%.3f' % res['macro_F1'],
          {o: res[o]['F1'] for o in OPS})

prev = {}
import os as _os
_pj = os.path.join(ROOT, '_review', 'exp_j_perop_prf.json')
if _os.path.exists(_pj):
    prev = json.load(open(_pj))
prev.update(out)
json.dump(prev, open(_pj, 'w'), indent=1)
print('saved exp_j_perop_prf.json')
