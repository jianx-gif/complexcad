# -*- coding: utf-8 -*-
"""Balancing supplement, stage 2: choose the sweep/loft programs and fetch their upstream
rows (code, 8 renders, STL, STEP, operation log) into output_supp/<uuid>/ in the layout
of output/<uuid>/ (导师 2026-09-28: 补采 sweep/loft 样本).

Selection (seed 42): candidates from _review/supp_candidates.jsonl (stage 1), programs that
use BOTH operations first, then loft-only and sweep-only ones, drawn at random until the
share of sweep and of loft in (base 10000 + supplement) both reach TARGET (10.5 %, a margin
over R3's 10 % for execution or drawing failures). The base shares are counted from
output/<uuid>/description.json (3D operation counts).
Usage (base python, pyarrow + fsspec):  python -X utf8 supp_fetch_100k.py [--dry]
"""
import io, json, os, random, sys, time, collections

ROOT = r'E:/3005/data'
BASE = os.path.join(ROOT, 'output')
SUPP = os.path.join(ROOT, 'output_supp')
CAND = os.path.join(ROOT, '_review', 'supp_candidates.jsonl')
SEL = os.path.join(ROOT, '_review', 'supp_selection.json')
REPO = 'ADSKAILab/Zero-To-CAD-100k'
RES = 'https://huggingface.co/datasets/%s/resolve/main/' % REPO
UA = {'User-Agent': 'Mozilla/5.0 (thesis data check)'}
TARGET = 0.105
SEED = 42


def base_counts():
    n = sw = lo = 0
    for u in os.listdir(BASE):
        p = os.path.join(BASE, u, 'description.json')
        if not os.path.isfile(p):
            continue
        n += 1
        oc = json.load(open(p, encoding='utf-8')).get('operation_counts') or {}
        sw += 'sweep' in oc; lo += 'loft' in oc
    return n, sw, lo


def select():
    n0, sw0, lo0 = base_counts()
    print('base: n=%d sweep=%d (%.1f%%) loft=%d (%.1f%%)' % (n0, sw0, 100 * sw0 / n0, lo0, 100 * lo0 / n0))
    base_uuids = set(os.listdir(BASE))
    cands = [json.loads(l) for l in io.open(CAND, encoding='utf-8')]
    seen = set(); uniq = []
    for c in cands:
        if c['uuid'] in seen or c['uuid'] in base_uuids:
            continue
        seen.add(c['uuid']); uniq.append(c)
    both = [c for c in uniq if c['sweep'] and c['loft']]
    loft = [c for c in uniq if c['loft'] and not c['sweep']]
    sweep = [c for c in uniq if c['sweep'] and not c['loft']]
    rnd = random.Random(SEED)
    rnd.shuffle(both); rnd.shuffle(loft); rnd.shuffle(sweep)
    print('candidates: both=%d loft-only=%d sweep-only=%d' % (len(both), len(loft), len(sweep)))
    chosen = []; n, sw, lo = n0, sw0, lo0
    pools = {'both': both, 'loft': loft, 'sweep': sweep}
    while True:
        share_sw, share_lo = sw / n, lo / n
        if share_sw >= TARGET and share_lo >= TARGET:
            break
        if pools['both'] and (share_sw < TARGET and share_lo < TARGET):
            c = pools['both'].pop()
        elif share_lo < TARGET and pools['loft']:
            c = pools['loft'].pop()
        elif share_sw < TARGET and pools['sweep']:
            c = pools['sweep'].pop()
        elif pools['both']:
            c = pools['both'].pop()
        else:
            print('pools exhausted'); break
        chosen.append(c); n += 1; sw += c['sweep']; lo += c['loft']
    print('chosen: %d programs (sweep %d, loft %d, both %d) -> combined n=%d sweep %.2f%% loft %.2f%%' % (
        len(chosen), sum(c['sweep'] for c in chosen), sum(c['loft'] for c in chosen),
        sum(c['sweep'] and c['loft'] for c in chosen), n, 100 * sw / n, 100 * lo / n))
    sel = {'seed': SEED, 'target_share': TARGET, 'base': {'n': n0, 'sweep': sw0, 'loft': lo0},
           'candidates': {'both': len(both) + sum(c['sweep'] and c['loft'] for c in chosen),
                          'loft_only': len(loft) + sum(c['loft'] and not c['sweep'] for c in chosen),
                          'sweep_only': len(sweep) + sum(c['sweep'] and not c['loft'] for c in chosen)},
           'chosen': [{k: c[k] for k in ('uuid', 'file', 'rg', 'row', 'sweep', 'loft')} for c in chosen]}
    json.dump(sel, open(SEL, 'w'), indent=1)
    return sel


def fetch(sel):
    import fsspec, pyarrow.parquet as pq
    fs = fsspec.filesystem('https', client_kwargs={'headers': UA})
    groups = collections.defaultdict(list)
    for c in sel['chosen']:
        groups[(c['file'], c['rg'])].append(c)
    os.makedirs(SUPP, exist_ok=True)
    t0 = time.time(); done = 0; written = 0
    for gi, ((path, rg), rows) in enumerate(sorted(groups.items())):
        want = {c['uuid'] for c in rows}
        if all(os.path.isfile(os.path.join(SUPP, u, 'model.step')) for u in want):
            done += len(want); continue
        for attempt in range(4):
            try:
                with fs.open(RES + path, 'rb', block_size=8 * 1024 * 1024) as fh:
                    pf = pq.ParquetFile(fh)
                    tb = pf.read_row_group(rg).to_pylist()
                break
            except Exception as e:
                print('retry', path, rg, attempt, repr(e)[:100], flush=True); time.sleep(5 * (attempt + 1))
        else:
            print('GIVE UP', path, rg, flush=True); continue
        for row in tb:
            u = row['uuid']
            if u not in want:
                continue
            d = os.path.join(SUPP, u); os.makedirs(d, exist_ok=True)
            code = row['cadquery_file']
            if isinstance(code, bytes):
                code = code.decode('utf-8', 'replace')
            io.open(os.path.join(d, 'cadquery.py'), 'w', encoding='utf-8', newline='\n').write(code)
            for k in range(8):
                im = row.get('image_%d' % k)
                if isinstance(im, dict):
                    im = im.get('bytes')
                if im:
                    open(os.path.join(d, 'image_%d.png' % k), 'wb').write(im)
            open(os.path.join(d, 'model.stl'), 'wb').write(row['stl_file'])
            open(os.path.join(d, 'model.step'), 'wb').write(row['step_file'])
            try:
                ops = json.loads(row['cadquery_ops_json'])
            except Exception:
                ops = row['cadquery_ops_json']
            meta = {'uuid': u, 'num_faces': row['num_faces'], 'face_latency_ms': row['face_latency_ms'],
                    'cadquery_ops_json': ops, 'cadquery_ops_count': row['cadquery_ops_count'],
                    'ops_latency_ms': row['ops_latency_ms'], 'num_renders': row['num_renders'],
                    'source': {'dataset': REPO, 'split': 'train', 'file': path, 'row_group': rg}}
            json.dump(meta, open(os.path.join(d, 'metadata.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
            written += 1
        done += len(want)
        print('%3d/%d groups | %d/%d parts | %.0fs' % (gi + 1, len(groups), done, len(sel['chosen']), time.time() - t0), flush=True)
    print('DONE written=%d' % written, flush=True)


if __name__ == '__main__':
    sel = json.load(open(SEL)) if os.path.isfile(SEL) else select()
    if '--dry' not in sys.argv:
        fetch(sel)
