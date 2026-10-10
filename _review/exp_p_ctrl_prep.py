# -*- coding: utf-8 -*-
"""闭环对照组数据: 与 ComplexCAD 微调集同样数量 (7768 train + 100 val) 的 CAD-Recode v1.5 训练程序
(仅 sketch-extrude), 执行导出 STL, 组织成同一 CadRecodeDataset 格式 -> _review/cc_ctrl/.
用同一配方微调, 用来区分"复杂操作数据"与"再训练一会儿/适应评测框架"两个效应.
用法 (cadquery env): python exp_p_ctrl_prep.py
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
_DS = _os.environ.get('CADRECODE_DATASETS') or _ROOT + '/datasets'  # CAD-Recode dataset copies, see README
import os, sys, random, pickle, json, subprocess, time
from multiprocessing import Pool
ROOT = _ROOT
REPO = _DS + '/cadrecode_v15_train'
DST = os.path.join(ROOT, '_review', 'cc_ctrl')
MESH = os.path.join(DST, 'mesh'); CODE = os.path.join(DST, 'code')
N_TRAIN, N_VAL, SEED = 7768, 100, 7


def run_one(args):
    rel, name = args
    out_stl = os.path.join(MESH, name + '.stl'); out_py = os.path.join(CODE, name + '.py')
    if os.path.exists(out_stl) and os.path.exists(out_py):
        return name, True
    try:
        import cadquery as cq
        src = open(os.path.join(REPO, rel), encoding='utf-8', errors='replace').read()
        g = {'cq': cq, '__name__': '__cqx__'}
        exec(src, g)
        r = g.get('r') or g.get('result')
        if r is None:
            for v in g.values():
                if isinstance(v, cq.Workplane):
                    r = v
        s = r.val() if hasattr(r, 'val') else r
        if s is None or s.Volume() <= 1e-6:
            return name, False
        cq.exporters.export(cq.Workplane().add(s), out_stl, tolerance=0.05, angularTolerance=0.1)
        open(out_py, 'w', encoding='utf-8', newline='\n').write(src if src.endswith('\n') else src + '\n')
        return name, True
    except Exception:
        return name, False


def main():
    os.makedirs(MESH, exist_ok=True); os.makedirs(CODE, exist_ok=True)
    tree = subprocess.run(['git', '-C', REPO, 'ls-tree', '-r', '--name-only', 'HEAD', '--', 'train'],
                          capture_output=True, text=True).stdout.splitlines()
    pys = [p for p in tree if p.endswith('.py')]
    rnd = random.Random(SEED); rnd.shuffle(pys)
    cand = pys[:int((N_TRAIN + N_VAL) * 1.15)]
    jobs = [(p, os.path.splitext(os.path.basename(p))[0] + '_' + p.split('/')[-2]) for p in cand]
    ok = []; fail = 0; t0 = time.time()
    with Pool(4) as pool:
        for i, (name, good) in enumerate(pool.imap_unordered(run_one, jobs, chunksize=8)):
            if good:
                ok.append(name)
            else:
                fail += 1
            if i % 500 == 0:
                print('  %d done, ok %d, fail %d, %.0fs' % (i, len(ok), fail, time.time() - t0), flush=True)
            if len(ok) >= N_TRAIN + N_VAL:
                pool.terminate(); break
    ok = sorted(ok)[:N_TRAIN + N_VAL]
    rnd.shuffle(ok)
    for split, names in (('train', ok[N_VAL:]), ('val', ok[:N_VAL])):
        ann = [{'mesh_path': os.path.join(MESH, n + '.stl'), 'py_path': os.path.join(CODE, n + '.py'), 'uuid': n} for n in names]
        pickle.dump(ann, open(os.path.join(DST, f'{split}.pkl'), 'wb'))
        print(split, len(ann))
    json.dump(dict(source='filapro/cad-recode-v1.5 train (git 4696421)', seed=SEED, n_train=N_TRAIN, n_val=N_VAL,
                   executed_ok=len(ok), exec_failures=fail), open(os.path.join(DST, 'prep_stats.json'), 'w'), indent=1)
    print('DONE', flush=True)


if __name__ == '__main__':
    main()
