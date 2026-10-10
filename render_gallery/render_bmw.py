# -*- coding: utf-8 -*-
"""Seeded best / median / worst qualitative figure (annotation p58): among the executing predictions of a method on the
400-model subset, draw one case at random (seed 42) from the best decile, the middle decile and the worst decile of
Chamfer Distance; render GT vs prediction with the same lambert renderer as the other qualitative figures.
Run with cadfit-env python (trimesh + matplotlib); the prediction is executed with the cadquery env via real_root/exec_pred.py."""
import os as _os
import sys as _sys
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, sys, json, random, subprocess
# reuse the renderer definitions without running the module's top-level figure generation
_src = open(_ROOT + '/render_gallery/render_thesis_figs.py', encoding='utf-8').read()
_src = _src[:_src.index('_rm = {')]
exec(compile(_src, 'render_thesis_figs_defs', 'exec'))
BILD = _ROOT + '/_rev_clone/bilder'
PY = (_os.environ.get('COMPLEXCAD_PY_CADQUERY') or _sys.executable)
ENV = dict(os.environ)
_root = os.path.dirname(PY)
ENV['PATH'] = os.pathsep.join([_root, os.path.join(_root, 'Library', 'bin'), os.path.join(_root, 'Scripts'), ENV.get('PATH', '')])


def exec_pred(pyfile, out_stl):
    if os.path.isfile(out_stl):
        return True
    r = subprocess.run([PY, '-X', 'utf8', f'{ROOT}/real_root/exec_pred.py', pyfile, out_stl], capture_output=True, timeout=120, env=ENV)
    return r.returncode == 0 and os.path.isfile(out_stl)


def make(meth, label, out_png, seed=42):
    metrics = [json.loads(l) for l in open(f'{ROOT}/1m_Convert/precision_report/pred_metrics_{meth}.jsonl', encoding='utf-8')]
    ok = sorted([m for m in metrics if m.get('status') == 'ok' and m.get('chamfer') is not None], key=lambda m: m['chamfer'])
    n = len(ok); dec = max(1, n // 10)
    rng = random.Random(seed)
    picks = [('best decile', rng.choice(ok[:dec])), ('median decile', rng.choice(ok[n // 2 - dec // 2: n // 2 + dec // 2 + 1])), ('worst decile', rng.choice(ok[-dec:]))]
    cases = []; rec = []
    for tag, m in picks:
        u = m['uuid']; pred_py = f'{ROOT}/predictions/{meth}/{u}.py'; pred_stl = f'{TMP}/{meth}_bmw_{u[:8]}.stl'
        if not exec_pred(pred_py, pred_stl):
            print('exec fail', u); continue
        gt_ops = fmt(ops_of(f'{ROOT}/output/{u}/cadquery.py')); pr_ops = fmt(ops_of(pred_py))
        cases.append((f'{ROOT}/output/{u}/model.stl', gt_ops, pred_stl, pr_ops, '%s  %s  CD=%.3f' % (tag, u[:8], m['chamfer'])))
        rec.append(dict(tag=tag, uuid=u, chamfer=m['chamfer'], gt_ops=gt_ops, pred_ops=pr_ops))
        print(tag, u[:8], 'CD=%.3f' % m['chamfer'], '| GT:', gt_ops, '| PRED:', pr_ops)
    two_rows(cases, out_png, 'GT', label)
    json.dump(dict(method=meth, seed=seed, n_executing=n, decile=dec, cases=rec), open(out_png.replace('.png', '.json'), 'w'), indent=1)


if __name__ == '__main__':
    make('cadrecode', 'CAD-Recode', f'{BILD}/cmp_cadrecode_bmw.png')
    make('cadrille_cc', 'cadrille + ComplexCAD', f'{BILD}/cmp_cc_bmw.png')
