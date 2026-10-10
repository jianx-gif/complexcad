# -*- coding: utf-8 -*-
"""实验I: 去重后检索基线 (批注p55).
对每个测试件, 在体素描述子余弦<=0.99 的池样本中取最近邻(剔除近重复),
预测=所选池样本的GT程序 -> predictions/retrieval_dedup/<test_uuid>.py
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, glob, json, shutil
import numpy as np

ROOT = _ROOT
OUT = os.path.join(ROOT, 'output')
PRED = os.path.join(ROOT, 'predictions', 'retrieval_dedup')
G, THR = 10, 0.99
os.makedirs(PRED, exist_ok=True)

test = [l.strip() for l in open(os.path.join(ROOT, 'predictions', 'test_subset.txt'), encoding='utf-8') if l.strip()]
test_set = set(test)
pool = [os.path.basename(os.path.normpath(d)) for d in sorted(glob.glob(os.path.join(OUT, '*/')))
        if os.path.isfile(os.path.join(d, 'point_cloud.npy'))]
pool = [u for u in pool if u not in test_set]

def desc(u):
    p = np.load(os.path.join(OUT, u, 'point_cloud.npy'))[:, :3].astype(np.float32)
    c = p.mean(0); diag = float(np.linalg.norm(p.max(0) - p.min(0))) + 1e-9
    q = (p - c) / diag + 0.5
    idx = np.clip((q * G).astype(np.int32), 0, G - 1)
    v = np.zeros((G, G, G), np.float32); v[idx[:, 0], idx[:, 1], idx[:, 2]] = 1
    v = v.ravel(); return v / (np.linalg.norm(v) + 1e-9)

print('pool descriptors...', len(pool), flush=True)
P = np.stack([desc(u) for u in pool])
excluded = 0
for i, u in enumerate(test, 1):
    s = P @ desc(u)
    mask = s <= THR
    excluded += int((~mask).sum() > 0)
    j = int(np.argmax(np.where(mask, s, -1)))
    shutil.copyfile(os.path.join(OUT, pool[j], 'cadquery.py'),
                    os.path.join(PRED, u + '.py'))
    if i % 100 == 0:
        print(i, '/', len(test), flush=True)
print('DONE; test items that had >=1 excluded near-dup:', excluded, '/', len(test))
