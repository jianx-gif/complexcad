"""Evaluate predictions of the released cadrille checkpoint on the official DeepCAD/Text2CAD test
subsets, on Windows, with two conventions:

  --conv official : cadrille's own metrics, imported from E:/3005/data/cadrille_repro/evaluate.py
                    (py_file_to_mesh_and_brep_files -> tessellate(0.001, 0.1) -> STL; pred mesh
                    centred, scaled to unit max-extent and shifted to [0,1]^3; CD = sum of mean
                    squared NN distances on n_points=8192 samples; IoU = mesh boolean IoU;
                    IR = fraction with no CD). Aggregation copied from evaluate.run():
                    mean IoU over valid, median CD x1000, IR %, mean CD x1000 with skip 0..4.
                    Deviation from evaluate.py: on Windows a fresh process per exec with a 3 s
                    join is not feasible (spawn re-imports cadquery, ~5 s), so exec runs inside
                    persistent pool workers with a per-item timeout (default 180 s); the stale
                    global 'r' is cleared before each exec so a failed program cannot inherit the
                    previous item's solid.
  --conv ours     : E:/3005/data/1m_Convert/koor/eval_predictions.py convention (exec_shape,
                    validity = >=1 solid with volume > 1e-9, sample_surface, geom_metrics with
                    per-object bbox normalisation, Chamfer = mean L1 NN both ways, F-score@0.02,
                    op_recovery vs GT CadQuery program when available). GT points: 8192 samples
                    of the official GT STL (eval_predictions uses the GT point_cloud.npy).

Run with the cadfit-env python (CadQuery 2.6.1 / trimesh 4.11.5), as eval_predictions.py is.
"""
import os, sys, json, time, argparse
import multiprocessing as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPRO = 'E:/3005/data/cadrille_repro'
KOOR = 'E:/3005/data/1m_Convert/koor'
GT_MESH = os.path.join(HERE, 'data', 'deepcad_test_mesh_all')
GT_CODE = os.path.join(HERE, 'data', 'cadquery')


def _init(conv):
    global ev, ep, trimesh, cq
    import trimesh  # noqa
    if conv == 'official':
        sys.path.insert(0, REPRO)
        import evaluate as ev  # noqa  (imports cadquery)
    else:
        sys.path.insert(0, KOOR)
        import eval_predictions as ep  # noqa
        ep._winit()


def task_official(a):
    py_file_name, pred_py_path, pred_mesh_path, n_points = a
    t0 = time.time()
    eval_file_name = py_file_name[:py_file_name.rfind('+')]
    py_path = os.path.join(pred_py_path, py_file_name)
    mesh_path = os.path.join(pred_mesh_path, py_file_name[:-3] + '.stl')
    brep_path = os.path.join(pred_mesh_path, py_file_name[:-3] + '.step')
    if os.path.isfile(mesh_path):
        os.remove(mesh_path)
    ev.__dict__.pop('r', None)          # no leakage of the previous item's solid
    ev.py_file_to_mesh_and_brep_files(py_path, mesh_path, brep_path)
    executed = os.path.isfile(mesh_path)
    cd, iou = None, None
    try:
        pred_mesh = trimesh.load_mesh(mesh_path)
        center = (pred_mesh.bounds[0] + pred_mesh.bounds[1]) / 2.0
        pred_mesh.apply_translation(-center)
        extent = np.max(pred_mesh.extents)
        if extent > 1e-7:
            pred_mesh.apply_scale(1.0 / extent)
        pred_mesh.apply_transform(trimesh.transformations.translation_matrix([0.5, 0.5, 0.5]))
        gt_mesh = trimesh.load_mesh(os.path.join(GT_MESH, eval_file_name + '.stl'))
        cd = ev.compute_chamfer_distance(gt_mesh, pred_mesh, n_points)
        iou = ev.compute_iou(gt_mesh, pred_mesh)
    except Exception:
        pass
    index = py_file_name[len(eval_file_name) + 1:-3]
    return dict(file_name=eval_file_name, id=index, cd=None if cd is None else float(cd),
                iou=None if iou is None else float(iou), executed=executed,
                seconds=round(time.time() - t0, 2))


def task_ours(a):
    py_file_name, pred_py_path, _unused, n_points = a
    t0 = time.time()
    uid = py_file_name[:py_file_name.rfind('+')]
    rec = {'uuid': uid}
    try:
        code = open(os.path.join(pred_py_path, py_file_name), encoding='utf-8').read()
        gt_code_path = os.path.join(GT_CODE, uid + '.py')
        if os.path.isfile(gt_code_path):
            gt_ops = ep.parse_ops(open(gt_code_path, encoding='utf-8').read()) or []
            rec['gt_ops'] = gt_ops
            rec['complex'] = any(o in ep.COMPLEX for o in gt_ops)
        pred_ops = ep.parse_ops(code)
        if pred_ops is not None:
            rec['pred_ops'] = pred_ops
            if 'gt_ops' in rec:
                rec.update(ep.op_recovery(pred_ops, rec['gt_ops']))
        shape = ep.exec_shape(code)
        if shape is None:
            return {**rec, 'valid': False, 'status': 'no_result', 'seconds': round(time.time() - t0, 2)}
        vol = shape.Volume() if hasattr(shape, 'Volume') else 0.0
        nsol = len(shape.Solids()) if hasattr(shape, 'Solids') else 0
        rec['valid'] = bool(nsol >= 1 and vol > 1e-9)
        if not rec['valid']:
            return {**rec, 'status': 'invalid_geom', 'seconds': round(time.time() - t0, 2)}
        pred_pc = ep.sample_surface(shape, n_points)
        if pred_pc is None:
            return {**rec, 'status': 'no_mesh', 'seconds': round(time.time() - t0, 2)}
        gt_mesh = trimesh.load_mesh(os.path.join(GT_MESH, uid + '.stl'))
        gt_pc, _ = trimesh.sample.sample_surface(gt_mesh, n_points, seed=ep.FSEED)
        rec.update(ep.geom_metrics(pred_pc, np.asarray(gt_pc, dtype=float)))
        return {**rec, 'status': 'ok', 'seconds': round(time.time() - t0, 2)}
    except SyntaxError as e:
        return {**rec, 'valid': False, 'status': 'syntax_error', 'err': str(e)[:80]}
    except Exception as e:
        return {**rec, 'valid': False, 'status': 'exec_error', 'err': f'{type(e).__name__}: {e}'[:80]}


def run_pool(conv, tasks, jobs, timeout):
    fn = task_official if conv == 'official' else task_ours
    results = {}
    remaining = list(tasks)
    n_timeout = 0
    while remaining:
        pool = mp.Pool(jobs, initializer=_init, initargs=(conv,))
        pending = [(t, pool.apply_async(fn, (t,))) for t in remaining]
        restart = False
        for i, (t, ar) in enumerate(pending):
            try:
                results[t[0]] = ar.get(timeout=timeout)
            except mp.TimeoutError:
                key = t[0][:t[0].rfind('+')]
                results[t[0]] = (dict(file_name=key, id='0', cd=None, iou=None, executed=False,
                                      timeout=True) if conv == 'official'
                                 else dict(uuid=key, valid=False, status='timeout'))
                n_timeout += 1
                print('  TIMEOUT', t[0], flush=True)
                restart = True
                break
            except Exception as e:
                key = t[0][:t[0].rfind('+')]
                results[t[0]] = (dict(file_name=key, id='0', cd=None, iou=None, executed=False,
                                      worker_error=str(e)[:80]) if conv == 'official'
                                 else dict(uuid=key, valid=False, status='worker_error', err=str(e)[:80]))
            if (i + 1) % 25 == 0:
                print('  %d/%d' % (len(results), len(tasks)), flush=True)
        if restart:
            pool.terminate(); pool.join()
            remaining = [t for t in remaining if t[0] not in results]
            continue
        pool.close(); pool.join()
        remaining = []
    return [results[t[0]] for t in tasks], n_timeout


def aggregate_official(recs):
    """Copy of evaluate.run() aggregation (one sample per file here)."""
    from collections import defaultdict
    metrics = defaultdict(lambda: defaultdict(list))
    for m in recs:
        if m['cd'] is not None:
            metrics[m['file_name']]['cd'].append(m['cd'])
        if m['iou'] is not None:
            metrics[m['file_name']]['iou'].append(m['iou'])
        metrics[m['file_name']]
    ir_cd, ir_iou, cd, iou = 0, 0, [], []
    for key, value in metrics.items():
        if len(value['cd']):
            cd.append(min(value['cd']))
        else:
            ir_cd += 1
        if len(value['iou']):
            iou.append(max(value['iou']))
        else:
            ir_iou += 1
    n = len(metrics)
    cd_sorted = sorted(cd)
    out = {
        'n': n,
        'n_valid_cd': len(cd), 'n_valid_iou': len(iou),
        'mean_iou_pct': float(np.mean(iou) * 100) if iou else None,
        'median_cd_x1000': float(np.median(cd) * 1000) if cd else None,
        'ir_pct': ir_cd / n * 100,
        'ir_iou_pct': ir_iou / n * 100,
        'mean_cd_x1000_skip': {str(i): float(np.mean(cd_sorted[:len(cd_sorted) - i]) * 1000)
                               for i in range(5) if len(cd_sorted) - i > 0},
        'iou_median_pct': float(np.median(iou) * 100) if iou else None,
        'iou_std_pct': float(np.std(iou) * 100) if iou else None,
        'cd_x1000_mean': float(np.mean(cd) * 1000) if cd else None,
        'cd_x1000_p25': float(np.percentile(cd, 25) * 1000) if cd else None,
        'cd_x1000_p75': float(np.percentile(cd, 75) * 1000) if cd else None,
        'executed_pct': float(np.mean([bool(r.get('executed')) for r in recs]) * 100),
        'iou_ge_0.9_pct': float(np.mean([x >= 0.9 for x in iou]) * 100) if iou else None,
        'iou_ge_0.5_pct': float(np.mean([x >= 0.5 for x in iou]) * 100) if iou else None,
    }
    return out


def aggregate_ours(recs):
    ok = [r for r in recs if r.get('status') == 'ok']
    def mean(xs):
        xs = [x for x in xs if x is not None]
        return float(np.mean(xs)) if xs else None
    from collections import Counter
    return {
        'n': len(recs),
        'valid_pct': 100 * mean([bool(r.get('valid', False)) for r in recs]),
        'chamfer_mean': mean([r.get('chamfer') for r in ok]),
        'chamfer_median': float(np.median([r['chamfer'] for r in ok])) if ok else None,
        'fscore_mean': mean([r.get('fscore') for r in ok]),
        'op_type_recall_mean': mean([r.get('op_type_recall') for r in recs if 'gt_ops' in r]),
        'op_count_recall_mean': mean([r.get('op_count_recall') for r in recs if 'gt_ops' in r]),
        'op_exact_pct': 100 * mean([r.get('op_exact') for r in recs if 'gt_ops' in r and 'op_exact' in r]),
        'n_with_gt_program': sum('gt_ops' in r for r in recs),
        'status_counts': dict(Counter(r.get('status') for r in recs)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--conv', choices=['official', 'ours'], required=True)
    ap.add_argument('--pred-dir', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--timeout', type=int, default=180)
    ap.add_argument('--n-points', type=int, default=8192)
    args = ap.parse_args()
    files = sorted(f for f in os.listdir(args.pred_dir) if f.endswith('.py'))
    mesh_dir = os.path.join(os.path.dirname(os.path.abspath(args.out)),
                            'tmp_mesh_' + os.path.basename(args.pred_dir))
    os.makedirs(mesh_dir, exist_ok=True)
    tasks = [(f, args.pred_dir, mesh_dir, args.n_points) for f in files]
    print('conv', args.conv, 'files', len(files), 'jobs', args.jobs, flush=True)
    t0 = time.time()
    recs, n_timeout = run_pool(args.conv, tasks, args.jobs, args.timeout)
    agg = aggregate_official(recs) if args.conv == 'official' else aggregate_ours(recs)
    agg['n_timeout'] = n_timeout
    agg['eval_seconds'] = round(time.time() - t0, 1)
    json.dump({'summary': agg, 'per_item': recs}, open(args.out, 'w'), indent=1)
    print(json.dumps(agg, indent=1), flush=True)


if __name__ == '__main__':
    mp.freeze_support()
    main()
