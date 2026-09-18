# -*- coding: utf-8 -*-
"""严格版逐操作 F1: 不可执行的预测视为未恢复任何操作 (代码级 F1 的保守对照). 输出 exp_j_strict.json."""
import json, os, sys
sys.path.insert(0, r'E:/3005/data/1m_Convert/koor')
from eval_predictions import parse_ops
ROOT = r'E:/3005/data'; OPS = ['loft', 'revolve', 'sweep', 'chamfer', 'fillet']
gt = {}
for line in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8'):
    j = json.loads(line); gt[j['uuid']] = set(o.lower() for o in (j.get('ops') or []))
out = {}
for m in sys.argv[1:]:
    pm = os.path.join(ROOT, '1m_Convert', 'precision_report', 'pred_metrics_%s.jsonl' % m)
    if not os.path.exists(pm):
        continue
    st = {}
    for l in open(pm, encoding='utf-8'):
        r = json.loads(l); st[r['uuid']] = r.get('status')
    tp = {o: 0 for o in OPS}; fp = {o: 0 for o in OPS}; fn = {o: 0 for o in OPS}
    for u, s in st.items():
        code = open(os.path.join(ROOT, 'predictions', m, u + '.py'), encoding='utf-8', errors='replace').read()
        pred = set(o.lower() for o in (parse_ops(code) or [])) if s == 'ok' else set()
        for o in OPS:
            g, p = o in gt[u], o in pred
            if g and p: tp[o] += 1
            elif p and not g: fp[o] += 1
            elif g and not p: fn[o] += 1
    res = {}; f1s = []
    for o in OPS:
        P = tp[o] / max(1, tp[o] + fp[o]); R = tp[o] / max(1, tp[o] + fn[o]); F = 2 * P * R / max(1e-9, P + R)
        res[o] = dict(P=round(P, 3), R=round(R, 3), F1=round(F, 3)); f1s.append(F)
    res['macro_F1'] = round(sum(f1s) / 5, 3); out[m] = res
    print(m, 'STRICT macroF1=%.3f' % res['macro_F1'], {o: res[o]['F1'] for o in OPS})
pj = os.path.join(ROOT, '_review', 'exp_j_strict.json')
prev = json.load(open(pj)) if os.path.exists(pj) else {}
prev.update(out); json.dump(prev, open(pj, 'w'), indent=1)
