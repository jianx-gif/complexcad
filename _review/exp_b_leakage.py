# -*- coding: utf-8 -*-
"""实验B: 检索池泄漏检查 (批注p55).
1) 源码级: 规范化 cadquery.py 哈希, 测试集 vs 池 精确重复数.
2) 几何级: 与检索基线同款体素描述子, 每个测试件最近池样本的余弦相似度分布."""
import os, glob, json, hashlib, re
import numpy as np

ROOT = r'E:/3005/data'
OUT = os.path.join(ROOT, 'output')
G = 10

test = [l.strip() for l in open(os.path.join(ROOT, 'predictions', 'test_subset.txt'), encoding='utf-8') if l.strip()]
test_set = set(test)
all_uuids = [os.path.basename(os.path.normpath(d)) for d in sorted(glob.glob(os.path.join(OUT, '*/')))
             if os.path.isfile(os.path.join(d, 'point_cloud.npy'))]
pool = [u for u in all_uuids if u not in test_set]

# 1) 源码规范化哈希 (去空白/注释, 保留数值 -> 检测模板级重复)
WS = re.compile(r'\s+|#.*')
def code_hash(u):
    try:
        s = open(os.path.join(OUT, u, 'cadquery.py'), encoding='utf-8', errors='replace').read()
    except Exception:
        return None
    return hashlib.md5(WS.sub('', s).encode()).hexdigest()

pool_hashes = {}
for u in pool:
    h = code_hash(u)
    if h:
        pool_hashes.setdefault(h, []).append(u)
dup = sum(1 for u in test if code_hash(u) in pool_hashes)
print('测试集与池的规范化源码精确重复:', dup, '/', len(test))

# 2) 体素描述子最近邻相似度
def desc(u):
    p = np.load(os.path.join(OUT, u, 'point_cloud.npy'))[:, :3].astype(np.float32)
    c = p.mean(0); diag = float(np.linalg.norm(p.max(0) - p.min(0))) + 1e-9
    q = (p - c) / diag + 0.5
    idx = np.clip((q * G).astype(np.int32), 0, G - 1)
    v = np.zeros((G, G, G), np.float32); v[idx[:, 0], idx[:, 1], idx[:, 2]] = 1
    v = v.ravel(); return v / (np.linalg.norm(v) + 1e-9)

print('building pool descriptors...', len(pool))
P = np.stack([desc(u) for u in pool])
sims = []
for u in test:
    s = P @ desc(u)
    sims.append(float(s.max()))
sims = np.array(sims)
qs = {q: round(float(np.quantile(sims, q)), 4) for q in (0.05, 0.5, 0.95, 1.0)}
out = {'n_test': len(test), 'n_pool': len(pool), 'exact_code_dups': dup,
       'nn_cosine_quantiles': qs,
       'frac_above_0.99': round(float((sims > 0.99).mean()), 4),
       'frac_above_0.95': round(float((sims > 0.95).mean()), 4)}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(ROOT, '_review', 'exp_b_leakage.json'), 'w'), indent=1)
