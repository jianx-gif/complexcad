# -*- coding: utf-8 -*-
"""Balancing supplement, stage 1: scan the upstream Zero-To-CAD-100k TRAIN split on
Hugging Face for programs that use sweep or loft (导师 2026-09-28: 从上游公开 100k 程序
补采 sweep/loft 样本, 解决 R3 未达标与「未做数据平衡」).

Only the small columns (uuid, cadquery_file, cadquery_ops_json, num_faces,
cadquery_ops_count) are fetched per row group over HTTP range requests; the file
list is read from the HF API. Output:
  _review/supp_candidates.jsonl   one line per sweep/loft program
  _review/supp_scan_stats.json    per-file counts (rows, sweep, loft, both)
Usage (base python, needs pyarrow + fsspec):  python -X utf8 supp_scan_100k.py
"""
import io, json, os, sys, time, urllib.request

import fsspec
import pyarrow.parquet as pq

ROOT = r'E:/3005/data'
REPO = 'ADSKAILab/Zero-To-CAD-100k'
API = 'https://huggingface.co/api/datasets/%s/tree/main/data/train?limit=1000' % REPO
RES = 'https://huggingface.co/datasets/%s/resolve/main/' % REPO
UA = {'User-Agent': 'Mozilla/5.0 (thesis data check)'}
COLS = ['uuid', 'cadquery_file', 'cadquery_ops_json', 'num_faces', 'cadquery_ops_count']
OUT_JL = os.path.join(ROOT, '_review', 'supp_candidates.jsonl')
OUT_ST = os.path.join(ROOT, '_review', 'supp_scan_stats.json')


def main():
    req = urllib.request.Request(API, headers=UA)
    files = [x['path'] for x in json.load(urllib.request.urlopen(req, timeout=60)) if x['type'] == 'file']
    files.sort()
    print('train files:', len(files), flush=True)
    fs = fsspec.filesystem('https', client_kwargs={'headers': UA})
    done = set()
    if os.path.isfile(OUT_ST):
        try:
            done = set(json.load(open(OUT_ST))['files'])
        except Exception:
            done = set()
    stats = json.load(open(OUT_ST)) if done else {'files': {}, 'rows': 0, 'sweep': 0, 'loft': 0, 'both': 0}
    t0 = time.time()
    with open(OUT_JL, 'a', encoding='utf-8') as jl:
        for i, path in enumerate(files):
            if path in done:
                continue
            fst = {'rows': 0, 'sweep': 0, 'loft': 0, 'both': 0}
            for attempt in range(4):
                try:
                    with fs.open(RES + path, 'rb', block_size=4 * 1024 * 1024) as fh:
                        pf = pq.ParquetFile(fh)
                        for rg in range(pf.metadata.num_row_groups):
                            tb = pf.read_row_group(rg, columns=COLS).to_pylist()
                            for k, row in enumerate(tb):
                                fst['rows'] += 1
                                try:
                                    ops = {o.get('op_name') for o in json.loads(row['cadquery_ops_json'] or '[]')}
                                except Exception:
                                    ops = set()
                                sw, lo = 'sweep' in ops, 'loft' in ops
                                if not (sw or lo):
                                    continue
                                fst['sweep'] += sw; fst['loft'] += lo; fst['both'] += (sw and lo)
                                code = row['cadquery_file']
                                if isinstance(code, bytes):
                                    code = code.decode('utf-8', 'replace')
                                jl.write(json.dumps({'uuid': row['uuid'], 'file': path, 'rg': rg, 'row': k,
                                                     'sweep': sw, 'loft': lo, 'num_faces': row['num_faces'],
                                                     'ops_count': row['cadquery_ops_count'],
                                                     'ops_json': row['cadquery_ops_json'],
                                                     'code': code}) + '\n')
                    break
                except Exception as e:
                    print('retry', path, attempt, repr(e)[:120], flush=True)
                    time.sleep(5 * (attempt + 1))
                    fst = {'rows': 0, 'sweep': 0, 'loft': 0, 'both': 0}
            else:
                print('GIVE UP', path, flush=True)
                continue
            jl.flush()
            stats['files'][path] = fst
            for k in ('rows', 'sweep', 'loft', 'both'):
                stats[k] += fst[k]
            json.dump(stats, open(OUT_ST, 'w'), indent=1)
            print('%3d/%d %s rows=%d sweep=%d loft=%d | cum rows=%d sweep=%d loft=%d | %.0fs' % (
                i + 1, len(files), path.split('/')[-1][:28], fst['rows'], fst['sweep'], fst['loft'],
                stats['rows'], stats['sweep'], stats['loft'], time.time() - t0), flush=True)
    print('DONE', json.dumps({k: stats[k] for k in ('rows', 'sweep', 'loft', 'both')}), flush=True)


if __name__ == '__main__':
    main()
