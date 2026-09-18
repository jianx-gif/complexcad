# -*- coding: utf-8 -*-
"""实验E: 跨内核版本受控实验 (批注p44).
在当前解释器(由外层选择 env: OCP 7.8.1 或 7.7.2)下重执行 N 个程序,
记录 F/E/V 计数 -> 与 metadata 参考对比 + 两 env 互相对比.
用法: python exp_e_kernel_ab.py <tag> <n>
"""
import sys, os, json, glob, random, io, contextlib

ROOT = r'E:/3005/data'
tag, N = sys.argv[1], int(sys.argv[2])

# 固定种子取分层样本: 含 sweep/loft 的全部 + 随机补足
metrics = {}
for line in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8'):
    j = json.loads(line)
    metrics[j['uuid']] = j
rare = [u for u, j in metrics.items()
        if set(o.lower() for o in (j.get('ops') or [])) & {'sweep', 'loft'}]
rest = sorted(set(metrics) - set(rare))
random.seed(42)
sample = rare + random.sample(rest, max(0, N - len(rare)))
sample = sample[:max(N, len(rare))]

out_path = os.path.join(ROOT, '_review', f'exp_e_counts_{tag}.jsonl')
done = set()
if os.path.isfile(out_path):
    for line in open(out_path, encoding='utf-8'):
        try:
            done.add(json.loads(line)['uuid'])
        except Exception:
            pass

from OCP.TopExp import TopExp
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCP.TopTools import TopTools_IndexedMapOfShape

def counts(shape):
    # 跨 OCP 版本稳定: IndexedMapOfShape 按 TShape 去重, 不依赖 __hash__ 语义
    td = shape.wrapped if hasattr(shape, 'wrapped') else shape
    out = []
    for t in (TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX):
        m = TopTools_IndexedMapOfShape()
        TopExp.MapShapes_s(td, t, m)
        out.append(m.Extent())
    return out

fout = open(out_path, 'a', encoding='utf-8')
n_done = 0
for u in sample:
    if u in done:
        continue
    py = os.path.join(ROOT, 'output', u, 'cadquery.py')
    rec = {'uuid': u}
    try:
        src = open(py, encoding='utf-8', errors='replace').read()
        g = {'__name__': '__main__'}
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            exec(compile(src, py, 'exec'), g)
        res = g.get('result')
        shape = res.val() if hasattr(res, 'val') else res
        f, e, v = counts(shape)
        rec.update(status='ok', F=f, E=e, V=v)
    except Exception as ex:
        rec.update(status='error', err=type(ex).__name__)
    fout.write(json.dumps(rec) + '\n')
    fout.flush()
    n_done += 1
    if n_done % 100 == 0:
        print(tag, n_done, flush=True)
fout.close()
print('DONE', tag, 'wrote', n_done, 'sample_size', len(sample))
