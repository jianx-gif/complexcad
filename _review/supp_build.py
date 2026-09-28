# -*- coding: utf-8 -*-
"""Balancing supplement, stage 3: run the augmentation pipeline on output_supp/<uuid>/
(fetched by supp_fetch_100k.py) and validate each part.

Per part (worker pool, cadfit-env):
  1. validation: execute cadquery.py in this environment (guarded, 120 s), compare the
     face count with the upstream record and with the upstream STEP re-imported here
     (the L1 cross-environment agreement of the precision chapter, same three counts);
  2. augment_data.augment(uuid): point cloud (npy/ply), model.brep, geometry statistics,
     description.json/.txt (text modality, fixed generator);
  3. make_drawings.process(uuid): drawing.{png,svg,dxf} (ISO sheet).
Parts that fail step 1 or 2 are moved to output_supp_rejected/. Summary in
_review/supp_build_stats.json. Usage: python -X utf8 supp_build.py [--jobs N] [--limit N]
"""
import json, os, shutil, sys, time, traceback, collections
from multiprocessing import Pool

ROOT = r'E:/3005/data'
SUPP = os.path.join(ROOT, 'output_supp')
REJ = os.path.join(ROOT, 'output_supp_rejected')


def _init():
    os.chdir(ROOT); sys.path.insert(0, ROOT)
    import augment_data, make_drawings
    augment_data.OUT = 'output_supp'; make_drawings.OUT = 'output_supp'


def _exec_faces(code):
    """Execute the program in a fresh namespace; return (faces of `result`, error)."""
    import cadquery as cq
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE
    ns = {}
    try:
        exec(compile(code, '<cadquery>', 'exec'), ns)
    except Exception as e:
        return None, 'exec: %s' % repr(e)[:160]
    obj = ns.get('result')
    if obj is None:
        cands = [v for v in ns.values() if isinstance(v, cq.Workplane)]
        obj = cands[-1] if cands else None
    if obj is None:
        return None, 'no result object'
    try:
        shape = obj.val() if isinstance(obj, cq.Workplane) else obj
        w = shape.wrapped if hasattr(shape, 'wrapped') else shape
        n = 0; ex = TopExp_Explorer(w, TopAbs_FACE)
        while ex.More():
            n += 1; ex.Next()
        return n, None
    except Exception as e:
        return None, 'faces: %s' % repr(e)[:160]


def one(u):
    import augment_data, make_drawings
    d = os.path.join(SUPP, u)
    rec = {'uuid': u}
    t0 = time.time()
    try:
        meta = json.load(open(os.path.join(d, 'metadata.json'), encoding='utf-8'))
        code = open(os.path.join(d, 'cadquery.py'), encoding='utf-8').read()
        n_exec, err = _exec_faces(code)
        rec['faces_upstream'] = meta.get('num_faces'); rec['faces_exec'] = n_exec; rec['exec_error'] = err
        shape = augment_data.load_step(os.path.join(d, 'model.step'))
        rec['faces_step'] = augment_data._count_unique(shape, __import__('OCP.TopAbs', fromlist=['TopAbs_FACE']).TopAbs_FACE)
        rec['faces_agree'] = (n_exec is not None and n_exec == meta.get('num_faces') == rec['faces_step'])
        if n_exec is None:
            rec['status'] = 'reject_exec'
        else:
            augment_data.augment(u)
            try:
                make_drawings.process(u)
                rec['drawing'] = True
            except Exception as e:
                rec['drawing'] = False; rec['drawing_error'] = repr(e)[:160]
            desc = json.load(open(os.path.join(d, 'description.json'), encoding='utf-8'))
            rec['ops'] = desc.get('operation_counts')
            rec['status'] = 'ok'
    except Exception as e:
        rec['status'] = 'reject_error'; rec['error'] = repr(e)[:200]
    rec['seconds'] = round(time.time() - t0, 1)
    return rec


def main():
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 8
    limit = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else 0
    us = sorted(u for u in os.listdir(SUPP) if os.path.isfile(os.path.join(SUPP, u, 'model.step')))
    us = [u for u in us if not os.path.isfile(os.path.join(SUPP, u, 'drawing.dxf'))]
    if limit:
        us = us[:limit]
    print('parts to build:', len(us), flush=True)
    os.makedirs(REJ, exist_ok=True)
    recs = []
    t0 = time.time()
    with Pool(jobs, initializer=_init) as pool:
        for i, rec in enumerate(pool.imap_unordered(one, us, chunksize=4)):
            recs.append(rec)
            if rec['status'] != 'ok':
                src = os.path.join(SUPP, rec['uuid'])
                if os.path.isdir(src):
                    shutil.move(src, os.path.join(REJ, rec['uuid']))
            if (i + 1) % 25 == 0 or i + 1 == len(us):
                ok = sum(r['status'] == 'ok' for r in recs)
                print('%d/%d ok=%d %.0fs' % (i + 1, len(us), ok, time.time() - t0), flush=True)
    stat = collections.Counter(r['status'] for r in recs)
    ops = collections.Counter()
    for r in recs:
        if r['status'] == 'ok':
            for k in (r.get('ops') or {}):
                ops[k] += 1
    out = {'n': len(recs), 'status': dict(stat),
           'faces_agree': sum(bool(r.get('faces_agree')) for r in recs),
           'drawing_ok': sum(bool(r.get('drawing')) for r in recs),
           'ops_models_with': dict(ops), 'records': recs}
    json.dump(out, open(os.path.join(ROOT, '_review', 'supp_build_stats.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'records'}, indent=1))


if __name__ == '__main__':
    main()
