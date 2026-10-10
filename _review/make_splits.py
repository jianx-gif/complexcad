# -*- coding: utf-8 -*-
"""Official split files for the release (answering the p41 annotation).
test = the 400-model stratified evaluation subset; quarantine = executing models whose shape is a near-duplicate of a test
shape (same rule as exp_p_prep: 24^3 voxel-descriptor cosine > 0.90 AND normalised bidirectional Chamfer < 0.02);
val = the 100 seeded validation models of exp_p_prep; train = every other executing model (all program lengths).
Writes <repo>/splits/*.txt + splits.json.  Run with the cadfit-env python (scipy)."""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, sys, json, pickle
import numpy as np
from scipy.spatial import cKDTree
ROOT = _ROOT; OUT = os.path.join(ROOT, 'output'); D = os.path.join(ROOT, 'splits'); os.makedirs(D, exist_ok=True)
G = 24
metrics = {json.loads(l)['uuid']: json.loads(l) for l in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8')}
executed = sorted(u for u, r in metrics.items() if r['status'] == 'ok')
test = [l.strip() for l in open(os.path.join(ROOT, 'predictions', 'test_subset.txt')) if l.strip()]
val = [l.strip() for l in open(os.path.join(ROOT, '_review', 'cc_full', 'val_uuids.txt')) if l.strip()]
pool = [u for u in executed if u not in set(test)]


def load_pc(u):
    return np.load(os.path.join(OUT, u, 'point_cloud.npy'))[:, :3].astype(np.float32)


def norm(p):
    c = (p.min(0) + p.max(0)) / 2.0; s = float((p.max(0) - p.min(0)).max()) + 1e-9
    return (p - c) / s


def desc(p):
    q = norm(p) + 0.5
    idx = np.clip((q * G).astype(np.int32), 0, G - 1)
    v = np.zeros((G, G, G), np.float32); v[idx[:, 0], idx[:, 1], idx[:, 2]] = 1
    v = v.ravel(); return v / (np.linalg.norm(v) + 1e-9)


def cd(a, b):
    A, B = norm(a), norm(b)
    return float(cKDTree(B).query(A)[0].mean() + cKDTree(A).query(B)[0].mean())


print('descriptors ...', flush=True)
pcs = {u: load_pc(u) for u in pool}
P = np.stack([desc(pcs[u]) for u in pool])
excluded = {}
for i, t in enumerate(test):
    pt = load_pc(t); dt = desc(pt)
    s = P @ dt
    for j in np.where(s > 0.90)[0]:
        u = pool[j]
        if u in excluded:
            continue
        c = cd(pt, pcs[u])
        if c < 0.02:
            excluded[u] = (t, round(float(s[j]), 4), round(c, 5))
print('near-duplicates of test items:', len(excluded), flush=True)
dup = sorted(excluded)
train = sorted(u for u in pool if u not in excluded and u not in set(val))
test_exec = [t for t in test if t in set(executed)]
assert len(train) + len(val) + len(dup) + len(test_exec) == len(executed), 'counts do not reconcile'
for name, lst in (('test_400', test), ('val_100', val), ('train', train), ('quarantine_near_duplicates', dup)):
    open(os.path.join(D, name + '.txt'), 'w', newline='\n').write('\n'.join(lst) + '\n')
open(os.path.join(D, 'quarantine_pairs.json'), 'w').write(json.dumps({u: dict(test_uuid=t, cosine=s, chamfer=c) for u, (t, s, c) in excluded.items()}, indent=1))
non_exec = sorted(u for u, r in metrics.items() if r['status'] != 'ok')
open(os.path.join(D, 'non_executing_18.txt'), 'w', newline='\n').write('\n'.join(non_exec) + '\n')
json.dump(dict(rule='test = stratified 400 (seeded; 200 with loft/revolve/sweep, 200 without); quarantine = executing models whose 24^3 voxel-descriptor cosine > 0.90 to a test model AND normalised bidirectional Chamfer < 0.02 (identity noise floor 0.0163); val = 100 seeded from the remaining pool; train = all other executing models, all program lengths (the training experiments of Ch. 6 additionally cap comment-stripped programs at 1500 characters for GPU memory: 6171 train / 71 val); non_executing = the 18 programs that fail in the kernel (excluded from every split); assemblies inherit the split of their base part(s), two-part assemblies whose parts fall in different splits go to test' + '; the 20 programs of the upstream test split that were missing from the release until 2026-09-13 were restored on that date, after the training arms of Ch. 6 had been run, so none of them is in any arm\'s training data or in any seeded audit sample',
               counts=dict(test=len(test), test_executing=len(test_exec), val=len(val), train=len(train), quarantine=len(dup), non_executing=len(non_exec), total=len(metrics))),
          open(os.path.join(D, 'splits.json'), 'w'), indent=1)
print(json.load(open(os.path.join(D, 'splits.json')))['counts'])
