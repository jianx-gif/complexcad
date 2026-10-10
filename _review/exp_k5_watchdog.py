# -*- coding: utf-8 -*-
"""第5轮恒等重复: 分块看门狗驱动.
按500件一块调用 eval_predictions --self-test --names-file <chunk>, 每块硬超时;
超时块二分定位挂起件并跳过(记 skipped). 汇总口径与 summarize() 完全一致
(CD/F 对 status==ok 平均, valid 对全体平均).
"""
import os as _os
import sys as _sys
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, sys, json, subprocess, tempfile

ROOT = _ROOT
KOOR = os.path.join(ROOT, '1m_Convert', 'koor')
PY = (_os.environ.get('COMPLEXCAD_PY_CADFIT') or _sys.executable)
JSONL = os.path.join(ROOT, '1m_Convert', 'precision_report', 'pred_metrics_selftest.jsonl')
MERGED = os.path.join(ROOT, '_review', 'exp_k5_run5_records.jsonl')
CHUNK, TO_CHUNK, TO_ONE = 500, 420, 60

uuids = [json.loads(l)['uuid'] for l in
         open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8')]
print('total', len(uuids), flush=True)

done_uuids = set()
import os.path as _osp
if _osp.isfile(MERGED):
    for _l in open(MERGED, encoding='utf-8'):
        try: done_uuids.add(json.loads(_l)['uuid'])
        except Exception: pass
print('resume: already have', len(done_uuids))
merged = open(MERGED, 'a', encoding='utf-8')
skipped = []

def run_names(names, timeout):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write('\n'.join(names)); nf = f.name
    try:
        r = subprocess.run([PY, '-X', 'utf8', 'eval_predictions.py', '--self-test',
                            '--names-file', nf, '--jobs', '6'],
                           cwd=KOOR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
        ok = (r.returncode == 0)
    except subprocess.TimeoutExpired:
        subprocess.run(['powershell', '-Command',
                        "Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Id -ne %d} | Stop-Process -Force" % os.getpid()],
                       capture_output=True)
        ok = False
    finally:
        os.unlink(nf)
    if ok and os.path.isfile(JSONL):
        for l in open(JSONL, encoding='utf-8'):
            merged.write(l)
        merged.flush()
    return ok

def bisect(names):
    if len(names) == 1:
        if not run_names(names, TO_ONE):
            skipped.append(names[0])
            print('SKIP hang:', names[0], flush=True)
        return
    mid = len(names) // 2
    for half in (names[:mid], names[mid:]):
        if not half:
            continue
        if not run_names(half, max(TO_ONE, TO_CHUNK * len(half) // CHUNK + 60)):
            bisect(half)

for i in range(0, len(uuids), CHUNK):
    grp = [u for u in uuids[i:i + CHUNK] if u not in done_uuids]
    if not grp:
        print('chunk %d skip(done)' % i, flush=True); continue
    print('chunk %d-%d' % (i, i + len(grp)), flush=True)
    if not run_names(grp, TO_CHUNK):
        print('  chunk timeout -> bisect', flush=True)
        bisect(grp)
merged.close()

# 汇总(与 summarize 同口径)
recs = [json.loads(l) for l in open(MERGED, encoding='utf-8')]
seen = {}
for r in recs:
    seen[r['uuid']] = r
recs = list(seen.values())
ok = [r for r in recs if r.get('status') == 'ok']
def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / max(1, len(xs))
print('\nRUN5  N=%d (skipped %d: %s)' % (len(recs), len(skipped), skipped), flush=True)
print('  ALL valid=%.1f%%  CD=%.4f  F=%.3f  opType=%.2f exact=%.1f%%'
      % (100 * mean([bool(r.get('valid')) for r in recs]),
         mean([r.get('chamfer') for r in ok]),
         mean([r.get('fscore') for r in ok]),
         mean([r.get('op_type_recall') for r in recs]),
         100 * mean([r.get('op_exact') for r in recs])), flush=True)
