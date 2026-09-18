# -*- coding: utf-8 -*-
"""Retrieval baseline with the release quarantine applied to the pool (annotation #181, 2026-09-18):
the 271 executing models whose shape is a near-duplicate of a test shape (24^3 voxel cosine > 0.90 and
normalised Chamfer < 0.02, splits/quarantine_near_duplicates.txt) are removed from the retrieval pool;
otherwise identical to retrieval_baseline.py / exp_i (10^3 voxel descriptor, cosine nearest neighbour).
Predictions -> predictions/retrieval_noq/<test_uuid>.py ; summary -> _review/exp_i2_retrieval_noquarantine.json
"""
import os, glob, json, shutil
import numpy as np

ROOT = r'E:/3005/data'
OUT = os.path.join(ROOT, 'output')
PRED = os.path.join(ROOT, 'predictions', 'retrieval_noq')
G = 10
os.makedirs(PRED, exist_ok=True)

test = [l.strip() for l in open(os.path.join(ROOT, 'predictions', 'test_subset.txt'), encoding='utf-8') if l.strip()]
test_set = set(test)
quar = {l.strip() for l in open(os.path.join(ROOT, 'splits', 'quarantine_near_duplicates.txt'), encoding='utf-8') if l.strip()}
pool_all = [os.path.basename(os.path.normpath(d)) for d in sorted(glob.glob(os.path.join(OUT, '*/')))
            if os.path.isfile(os.path.join(d, 'point_cloud.npy'))]
pool_all = [u for u in pool_all if u not in test_set]
pool = [u for u in pool_all if u not in quar]
print('pool', len(pool_all), '-> without quarantine', len(pool), '(removed', len(pool_all) - len(pool), ')', flush=True)

def desc(u):
    p = np.load(os.path.join(OUT, u, 'point_cloud.npy'))[:, :3].astype(np.float32)
    c = p.mean(0); diag = float(np.linalg.norm(p.max(0) - p.min(0))) + 1e-9
    q = (p - c) / diag + 0.5
    idx = np.clip((q * G).astype(np.int32), 0, G - 1)
    v = np.zeros((G, G, G), np.float32); v[idx[:, 0], idx[:, 1], idx[:, 2]] = 1
    v = v.ravel(); return v / (np.linalg.norm(v) + 1e-9)

P = np.stack([desc(u) for u in pool])
changed = 0
old_dir = os.path.join(ROOT, 'predictions', 'retrieval')
for i, u in enumerate(test, 1):
    s = P @ desc(u)
    j = int(np.argmax(s))
    src = os.path.join(OUT, pool[j], 'cadquery.py')
    shutil.copyfile(src, os.path.join(PRED, u + '.py'))
    old = os.path.join(old_dir, u + '.py')
    if os.path.isfile(old) and open(old, encoding='utf-8', errors='replace').read() != open(src, encoding='utf-8', errors='replace').read():
        changed += 1
    if i % 100 == 0:
        print(i, '/', len(test), flush=True)
summary = {'pool_size_with_quarantine': len(pool_all), 'pool_size_without': len(pool), 'quarantined_removed': len(pool_all) - len(pool),
           'test_items_whose_neighbour_changed': changed, 'n_test': len(test), 'descriptor': '10^3 voxel occupancy, cosine', 'pred_dir': PRED}
json.dump(summary, open(os.path.join(ROOT, '_review', 'exp_i2_retrieval_noquarantine.json'), 'w'), indent=1)
print('DONE', summary)
