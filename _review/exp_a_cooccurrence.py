# -*- coding: utf-8 -*-
"""实验A: 五复杂操作共现矩阵 (批注p40/p47)."""
import json, collections, itertools

OPS = ['loft', 'revolve', 'sweep', 'chamfer', 'fillet']
pair = collections.Counter()
single = collections.Counter()
n = 0
for line in open(r'E:/3005/data/1m_Convert/precision_report/metrics.jsonl', encoding='utf-8'):
    j = json.loads(line); n += 1
    s = set(o.lower() for o in (j.get('ops') or [])) & set(OPS)
    for o in s:
        single[o] += 1
    for a, b in itertools.combinations(sorted(s), 2):
        pair[(a, b)] += 1

print('n =', n)
print('单操作模型数:', dict(single))
print('共现矩阵 (模型数):')
hdr = '{:>10}'.format('') + ''.join('{:>9}'.format(o) for o in OPS)
print(hdr)
for a in OPS:
    row = '{:>10}'.format(a)
    for b in OPS:
        if a == b:
            v = single[a]
        else:
            v = pair[tuple(sorted((a, b)))]
        row += '{:>9}'.format(v)
    print(row)
json.dump({'single': dict(single),
           'pairs': {f'{a}+{b}': v for (a, b), v in pair.items()}},
          open(r'E:/3005/data/_review/exp_a_cooccurrence.json', 'w'), indent=1)
