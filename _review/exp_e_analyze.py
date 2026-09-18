# -*- coding: utf-8 -*-
"""实验E分析: 两内核计数 vs metadata GT + 互相对比."""
import json, os

ROOT = r'E:/3005/data'
gt = {}
for line in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8'):
    j = json.loads(line)
    g = j.get('gt') or {}
    if g:
        gt[j['uuid']] = (g['num_faces'], g['num_edges'], g['num_vertices'])

def load(tag):
    out = {}
    p = os.path.join(ROOT, '_review', f'exp_e_counts_{tag}.jsonl')
    for line in open(p, encoding='utf-8'):
        j = json.loads(line)
        out[j['uuid']] = j
    return out

a = load('ocp781')
b = load('ocp772')
common = [u for u in a if u in b and a[u]['status'] == 'ok' and b[u]['status'] == 'ok' and u in gt]
errA = sum(1 for u in a.values() if u['status'] != 'ok')
errB = sum(1 for u in b.values() if u['status'] != 'ok')

def agree(rec, ref):
    return (rec['F'], rec['E'], rec['V']) == tuple(ref)

agA = sum(1 for u in common if agree(a[u], gt[u]))
agB = sum(1 for u in common if agree(b[u], gt[u]))
agAB = sum(1 for u in common if (a[u]['F'], a[u]['E'], a[u]['V']) == (b[u]['F'], b[u]['E'], b[u]['V']))
# 关键: A 与 GT 不一致的案例里, B 是否也以同样方式不一致?
misA = [u for u in common if not agree(a[u], gt[u])]
misA_sameAB = sum(1 for u in misA if (a[u]['F'], a[u]['E'], a[u]['V']) == (b[u]['F'], b[u]['E'], b[u]['V']))

res = {
    'n_a': len(a), 'n_b': len(b), 'n_common_ok': len(common),
    'exec_errors_a_ocp781': errA, 'exec_errors_b_ocp772': errB,
    'agree_gt_ocp781': round(agA / len(common), 4),
    'agree_gt_ocp772': round(agB / len(common), 4),
    'agree_between_kernels': round(agAB / len(common), 4),
    'gt_mismatch_ocp781': len(misA),
    'of_those_both_kernels_identical': misA_sameAB,
}
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(ROOT, '_review', 'exp_e_analysis.json'), 'w'), indent=1)
