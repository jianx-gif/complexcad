# -*- coding: utf-8 -*-
"""Re-render figures 6.1-6.5 from the exact B-rep (STEP) instead of STL meshes, with the same cases,
labels and layout as before (render_thesis_figs.py / render_bmw.py). Ground truth = output/<uuid>/model.step;
predictions are CadQuery programs executed to STEP. The GrabCAD inputs of fig. 6.5 exist only as meshes and
are rendered from their STL with the same shading (smooth normals, feature edges, no triangle lines).
Run with cadfit-env python. Old PNGs are kept as <name>.stl_version.png in render_gallery/."""
import os, re, json, shutil, sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_step as R

ROOT = 'E:/3005/data'
BILD = f'{ROOT}/_rev_clone/bilder'
GT_C, PR_C = '#4C9BE8', '#E8975A'
OPS_RE = re.compile(r"\.(revolve|sweep|loft|fillet|chamfer|extrude|shell|cut|union|add|hole|cskHole)\(", re.I)
LOG = []


def ops_of(pyfile):
    try:
        hits = OPS_RE.findall(open(pyfile, encoding='utf-8', errors='replace').read())
    except Exception:
        return {}
    cnt = {}
    for h in hits:
        cnt[h.lower()] = cnt.get(h.lower(), 0) + 1
    return cnt


def fmt(cnt):
    return '+'.join(f'{k}x{v}' if v > 1 else k for k, v in sorted(cnt.items())) or 'none'


def wrap_ops(label, width=26):
    if len(label) <= width:
        return label
    head, sep, ops = label.partition(': ')
    parts = ops.split('+') if sep else label.split('+')
    lines, cur = [], (head + ': ' if sep else '')
    for p in parts:
        tok = p if not cur or cur.endswith(': ') else '+' + p
        if cur and not cur.endswith(': ') and len(cur) + len(tok) > width:
            lines.append(cur + '+'); cur = p
        else:
            cur += tok
    lines.append(cur)
    return '\n'.join(lines)


def panel(ax, path, color, title, invalid_label=None):
    ax.set_axis_off()
    img = R.render(path, color) if path else None
    if img is None:
        ax.text(0.5, 0.5, f'{invalid_label or ""}\ninvalid\n(not executable)', ha='center', va='center',
                transform=ax.transAxes, fontsize=10, color='#993333')
        LOG.append(('invalid', path))
        return False
    ax.imshow(R.crop(img), interpolation='lanczos')
    ax.set_title(wrap_ops(title), fontsize=8.5)
    LOG.append(('ok', path))
    return True


def two_rows(cases, out, top_lab, bot_lab):
    """cases: [(top_path, top_ops, bot_path, bot_ops, subtitle)]"""
    fig, axes = plt.subplots(2, 3, figsize=(12, 8.4))
    for j, (tp, to, bp, bo, sub) in enumerate(cases):
        panel(axes[0, j], tp, GT_C, f'{top_lab}: {to}')
        axes[0, j].text(0.5, 1.22, sub, ha='center', transform=axes[0, j].transAxes, fontsize=9)
        panel(axes[1, j], bp, PR_C, f'{bot_lab}: {bo}', bot_lab)
    fig.tight_layout(h_pad=2.2)
    fig.savefig(out, dpi=140, bbox_inches='tight'); plt.close(fig)
    print('SAVED', out)


def backup(name):
    src = f'{BILD}/{name}'; dst = f'{ROOT}/render_gallery/{name[:-4]}.stl_version.png'
    if os.path.isfile(src) and not os.path.isfile(dst):
        shutil.copy(src, dst)


def uid(prefix, meth):
    import glob
    g = glob.glob(f'{ROOT}/predictions/{meth}/{prefix}*.py')
    return os.path.basename(g[0])[:-3] if g else None


def metric(meth, u):
    for l in open(f'{ROOT}/1m_Convert/precision_report/pred_metrics_{meth}.jsonl', encoding='utf-8'):
        j = json.loads(l)
        if j['uuid'] == u:
            return j
    return {}


# ---- 6.1 GT vs CADFit
backup('cmp_cadfit_qual.png')
CF = [('071a220d-5b4e-fc1d-c9ce-3a3a3b23b0ab', 'revolve + fillet + chamfer'),
      ('31d4bb86-0545-3475-30fa-96ba18d87b54', 'sweep + fillet + chamfer'),
      ('243ce854-9883-1843-c49b-d55366badb0c', 'loft')]
cases = []
for u, lab in CF:
    d = f'{ROOT}/cadfit_repro/cc_in_runs/{u}'
    cases.append((f'{ROOT}/output/{u}/model.step', fmt(ops_of(f'{ROOT}/output/{u}/cadquery.py')),
                  f'{d}/best_greedy_parallel_iterative.py', fmt(ops_of(f'{d}/best_greedy_parallel_iterative.py')), lab))
two_rows(cases, f'{BILD}/cmp_cadfit_qual.png', 'GT', 'CADFit')

# ---- 6.2 seeded best / median / worst of the ComplexCAD arm (first run, as the caption states)
backup('cmp_cc_bmw.png')
bmw = json.load(open(f'{BILD}/cmp_cc_bmw.json', encoding='utf-8'))
cases = []
for c in bmw['cases']:
    u = c['uuid']; pred = f'{ROOT}/predictions/cadrille_cc_run1_reinfer/{u}.py'
    cd = metric('cadrille_cc_run1_reinfer', u).get('chamfer', c['chamfer'])
    cases.append((f'{ROOT}/output/{u}/model.step', fmt(ops_of(f'{ROOT}/output/{u}/cadquery.py')),
                  pred, fmt(ops_of(pred)), '%s  %s  CD=%.3f' % (c['tag'], u[:8], cd)))
two_rows(cases, f'{BILD}/cmp_cc_bmw.png', 'GT', 'cadrille + ComplexCAD')

# ---- 6.3 retrieval and 6.4 CAD-Recode (same three cases as the captions)
for meth, prefixes, name, lab in (('retrieval', ['a1d1c4c1', 'fef3922d', '6a8c9b4a'], 'cmp_retrieval_qual.png', 'Retrieved'),
                                  ('cadrecode', ['77609f32', 'a1d1c4c1', '0afda985'], 'cmp_cadrecode_qual.png', 'CAD-Recode')):
    backup(name); cases = []
    for p in prefixes:
        u = uid(p, meth); pred = f'{ROOT}/predictions/{meth}/{u}.py'
        cd = metric(meth, u).get('chamfer')
        cases.append((f'{ROOT}/output/{u}/model.step', fmt(ops_of(f'{ROOT}/output/{u}/cadquery.py')),
                      pred, fmt(ops_of(pred)), '%s  CD=%.3f' % (u[:8], cd if cd is not None else -1)))
    two_rows(cases, f'{BILD}/{name}', 'GT', lab)

# ---- 6.5 real parts: input mesh (no B-rep exists) + three reconstructions from their programs
backup('cmp_real_qual.png')
RB = [('Ball_Stud_throttle', 'Ball stud (turned part)'),
      ('Assem_Connecting_Rod_-_Rod_Bearing-1', 'Rod bearing bushing'),
      ('C5_Knuckle_Mesh_Decimated', 'Steering knuckle')]
_rm = {(r['method'], r['part']): r for r in json.load(open(f'{ROOT}/real_root/real_metrics.json', encoding='utf-8'))}
def _ops_str(method, part):
    o = _rm.get((method, part), {}).get('ops', '')
    return '+'.join(t[:-2] if t.endswith('x1') else t for t in o.split()) or '?'
rows = [('Input', None, GT_C), ('CAD-Recode', 'cadrecode', PR_C), ('cadrille', 'cadrille', PR_C), ('CADFit', 'cadfit', PR_C)]
fig, axes = plt.subplots(4, 3, figsize=(12, 15.5))
for j, (n, lab) in enumerate(RB):
    for i, (rname, meth, col) in enumerate(rows):
        ax = axes[i, j]
        if meth is None:
            path, title = f'{ROOT}/cadfit_repro/grabcad_run/{n}.stl', 'Input mesh'
        elif meth == 'cadfit':
            path, title = f'{ROOT}/cadfit_repro/grabcad_run_runs/{n}/best_greedy_parallel_iterative.py', f"CADFit: {_ops_str('cadfit', n)}"
        else:
            path, title = f'{ROOT}/real_root/predictions/{meth}/{n}.py', f'{rname}: {_ops_str(meth, n)}'
            if not os.path.isfile(f'{ROOT}/real_root/pred_stl/{meth}/{n}.stl'):
                path = None          # was not executable in the evaluation either: keep the invalid panel
        panel(ax, path, col, title, rname)
        if i == 0:
            ax.text(0.5, 1.2, lab, ha='center', transform=ax.transAxes, fontsize=10, weight='bold')
fig.tight_layout(h_pad=2.0)
fig.savefig(f'{BILD}/cmp_real_qual.png', dpi=140, bbox_inches='tight'); plt.close(fig)
print('SAVED', f'{BILD}/cmp_real_qual.png')
json.dump(LOG, open(f'{ROOT}/render_gallery/_figtmp/step_render_log.json', 'w'), indent=1)
print('panels ok:', sum(1 for s, _ in LOG if s == 'ok'), 'invalid:', [p for s, p in LOG if s == 'invalid'])
