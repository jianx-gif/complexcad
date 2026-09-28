# -*- coding: utf-8 -*-
"""Figures 6.1-6.5 for the MDT-template version (_mdt_clone/bilder), six cases per figure.
Same STEP renders and colours as render_thesis_figs_step.py. The images hold only the renders with
(a)-(f) column tags and GT/method row tags; the operation lists, identifiers and Chamfer distances go
into a LaTeX table (bilder/<name>_ops.tex) that the figure environment inputs under the image.
Cases (a)-(c) are the ones of the earlier three-case figures; (d)-(f) are added:
  6.1 CADFit    : three further models of the 40-model CADFit stratum with loft / sweep+shell / loft
  6.2 seeded    : a second seeded draw (seed 42) per decile of the executing run-1 predictions
  6.3 retrieval : the two remaining prototype candidates of render_thesis_figs.py plus a swept part
  6.4 CAD-Recode: the two remaining prototype candidates plus a swept part
  6.5 real parts: all five GrabCAD parts of table 6.14 instead of three
Run with cadfit-env python. Writes nothing into _rev_clone."""
import os, re, json, sys, random
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_step as R

ROOT = 'E:/3005/data'
BILD = f'{ROOT}/_mdt_clone/bilder'
GT_C, PR_C = '#4C9BE8', '#E8975A'
FS = 1.9                      # in-image tag size (the images are placed at the full text width)
OPS_RE = re.compile(r"\.(revolve|sweep|loft|fillet|chamfer|extrude|shell|cut|union|add|hole|cskHole)\(", re.I)
LOG = []
ABC = 'abcdefgh'


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


def tex_ops(s):
    """'chamfer+cutx3+extrudex5' -> 'chamfer, cut ×3, extrude ×5' in LaTeX"""
    if not s or s == 'none':
        return 'none'
    out = []
    for tok in s.split('+'):
        m = re.fullmatch(r'([A-Za-z]+)x(\d+)', tok)
        out.append((m.group(1) + '\\,$\\times$' + m.group(2)) if m else tok)
    return ', '.join(out)


def tt(u8):
    return '\\texttt{' + u8 + '}'


def panel(ax, path, color, invalid_label=None):
    ax.set_axis_off()
    img = R.render(path, color) if path else None
    if img is None:
        ax.text(0.5, 0.5, f'{invalid_label or ""}\ninvalid\n(not executable)', ha='center', va='center',
                transform=ax.transAxes, fontsize=8 * FS, color='#993333')
        LOG.append(('invalid', path))
        return False
    ax.imshow(R.crop(img), interpolation='lanczos')
    LOG.append(('ok', path))
    return True


def write_table(tex_out, header, rows, first_w=1.3, cell_ws=None):
    """header: column titles (without the first column); rows: (row label, cells)"""
    cell_ws = cell_ws or [3.5] * len(header)
    spec = '@{}>{\\raggedright\\arraybackslash}p{%.1fcm}' % first_w + ''.join('>{\\raggedright\\arraybackslash}p{%.1fcm}' % w for w in cell_ws) + '@{}'
    lines = ['\\begin{tabular}{' + spec + '}', '\\toprule', ' & ' + ' & '.join(header) + ' \\\\', '\\midrule']
    for lab, cells in rows:
        lines.append(lab + ' & ' + ' & '.join(cells) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}']
    open(tex_out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('TABLE', tex_out)


def six_cases(cases, out, top_lab, bot_lab, case_names, extra_col=None, img_bot_lab=None):
    """cases: 6 x (top_path, top_ops, bot_path, bot_ops, cd); image = 2 rows x 6 columns (GT / method),
    table = one row per case. Cases are ordered by Chamfer Distance (ascending) inside every figure.
    img_bot_lab: short row tag in the image."""
    assert len(cases) == 6
    order = sorted(range(6), key=lambda k: (cases[k][4] if cases[k][4] is not None else 9e9))
    cases = [cases[k] for k in order]; case_names = [case_names[k] for k in order]
    if extra_col:
        extra_col = (extra_col[0], [extra_col[1][k] for k in order])
    print('ORDER', os.path.basename(out), [(ABC[i], case_names[i].replace('\\texttt{', '').rstrip('}'), '%.4f' % c[4]) for i, c in enumerate(cases)])
    tag = img_bot_lab or bot_lab
    # one row of cases: ground truth above, reconstruction below (2 x 6 panels)
    fig, axes = plt.subplots(2, 6, figsize=(18, 6.2))
    fig.subplots_adjust(left=0.055, right=0.995, top=0.90, bottom=0.01, wspace=0.06, hspace=0.10)
    for k, (tp, to, bp, bo, cd) in enumerate(cases):
        panel(axes[0, k], tp, GT_C)
        axes[0, k].set_title('(%s)' % ABC[k], fontsize=10 * FS, pad=10)
        panel(axes[1, k], bp, PR_C, tag)
    for i, lab in enumerate((top_lab, tag)):
        axes[i, 0].text(-0.16, 0.5, lab, rotation=90, ha='center', va='center', transform=axes[i, 0].transAxes, fontsize=10 * FS)
    fig.savefig(out, dpi=140, bbox_inches='tight'); plt.close(fig)
    print('SAVED', out)
    header = ([extra_col[0]] if extra_col else []) + [top_lab + ' program', bot_lab + ' program', 'Chamfer Dist.']
    # text width 14.6 cm minus the column gaps (6 pt each side): p-widths must sum to 13.1 cm (4 columns) / 12.9 cm (5)
    widths = ([2.2] if extra_col else []) + ([3.5, 3.5, 1.2] if extra_col else [4.7, 4.7, 1.5])
    rows = []
    for k, c in enumerate(cases):
        cells = ([extra_col[1][k]] if extra_col else []) + [tex_ops(c[1]), tex_ops(c[3]) if c[2] else 'invalid',
                                                            '%.3f' % c[4] if c[4] is not None else '--']
        rows.append(('(%s) %s' % (ABC[k], case_names[k]), cells))
    write_table(out[:-4] + '_ops.tex', header, rows, first_w=2.2, cell_ws=widths)


def uid(prefix, meth):
    import glob
    g = glob.glob(f'{ROOT}/predictions/{meth}/{prefix}*.py')
    return os.path.basename(g[0])[:-3] if g else None


def metrics(meth):
    return [json.loads(l) for l in open(f'{ROOT}/1m_Convert/precision_report/pred_metrics_{meth}.jsonl', encoding='utf-8')]


def metric(meth, u):
    for j in metrics(meth):
        if j['uuid'] == u:
            return j
    return {}


# ---- 6.1 GT vs CADFit: the three original models plus three from the same 40-model stratum
CF = ['071a220d', '31d4bb86', '243ce854', '42982cdc', '556e2de0', '3924cfa5']
cf_m = {m['uuid'][:8]: m for m in metrics('cadfit')}
cases, names = [], []
for p in CF:
    m = cf_m[p]; u = m['uuid']
    d = f'{ROOT}/cadfit_repro/cc_in_runs/{u}'
    cases.append((f'{ROOT}/output/{u}/model.step', fmt(ops_of(f'{ROOT}/output/{u}/cadquery.py')),
                  f'{d}/best_greedy_parallel_iterative.py', fmt(ops_of(f'{d}/best_greedy_parallel_iterative.py')), m['chamfer']))
    names.append(tt(u[:8]))
    print('6.1', u[:8], 'CD=%.3f' % m['chamfer'], 'GT', cases[-1][1], '| CADFit', cases[-1][3])
six_cases(cases, f'{BILD}/cmp_cadfit_qual.png', 'GT', 'CADFit', names)

# ---- 6.2 seeded deciles of the ComplexCAD arm (run 1): the three recorded cases, then a second seeded draw
bmw = json.load(open(f'{ROOT}/_rev_clone/bilder/cmp_cc_bmw.json', encoding='utf-8'))
run1 = sorted([m for m in metrics('cadrille_cc_run1_reinfer') if m.get('status') == 'ok' and m.get('chamfer') is not None], key=lambda m: m['chamfer'])
n = len(run1); dec = max(1, n // 10)
first = {c['uuid'] for c in bmw['cases']}
pools = {'best decile': run1[:dec], 'median decile': run1[n // 2 - dec // 2: n // 2 + dec // 2 + 1], 'worst decile': run1[-dec:]}
rng = random.Random(42)
second = {tag: rng.choice([m for m in pool if m['uuid'] not in first]) for tag, pool in pools.items()}
print('6.2 run-1 executing predictions: n=%d, decile size %d' % (n, dec))
sel = [(c['tag'], c['uuid']) for c in bmw['cases']] + [(tag, second[tag]['uuid']) for tag in ('best decile', 'median decile', 'worst decile')]
cases, names, tags = [], [], []
for tag, u in sel:
    pred = f'{ROOT}/predictions/cadrille_cc_run1_reinfer/{u}.py'
    cd = metric('cadrille_cc_run1_reinfer', u).get('chamfer')
    cases.append((f'{ROOT}/output/{u}/model.step', fmt(ops_of(f'{ROOT}/output/{u}/cadquery.py')), pred, fmt(ops_of(pred)), cd))
    names.append(tt(u[:8])); tags.append(tag)
    print('6.2', tag, u[:8], 'CD=%.3f' % cd, 'GT', cases[-1][1], '| pred', cases[-1][3])
six_cases(cases, f'{BILD}/cmp_cc_bmw.png', 'GT', 'cadrille + ComplexCAD', names, extra_col=('Draw', tags), img_bot_lab='cadrille')
json.dump(dict(base=bmw, second_draw=dict(seed=42, n_executing_run1=n, decile=dec,
               cases=[dict(tag=t, uuid=u) for t, u in sel[3:]])), open(f'{BILD}/cmp_cc_bmw_six.json', 'w'), indent=1)

# ---- 6.3 retrieval and 6.4 CAD-Recode: the three original cases, the two remaining prototype candidates and a swept part
for meth, prefixes, name, lab in (('retrieval', ['a1d1c4c1', 'fef3922d', '6a8c9b4a', '7049af79', '20f7c650', 'c366d8b2'], 'cmp_retrieval_qual.png', 'Retrieved'),
                                  ('cadrecode', ['77609f32', 'a1d1c4c1', '0afda985', 'c50da0b7', '925bbf47', 'b9a25f2d'], 'cmp_cadrecode_qual.png', 'CAD-Recode')):
    cases, names = [], []
    for p in prefixes:
        u = uid(p, meth); pred = f'{ROOT}/predictions/{meth}/{u}.py'
        cd = metric(meth, u).get('chamfer')
        cases.append((f'{ROOT}/output/{u}/model.step', fmt(ops_of(f'{ROOT}/output/{u}/cadquery.py')), pred, fmt(ops_of(pred)), cd))
        names.append(tt(u[:8]))
        print(name[:-4], u[:8], 'CD=%.3f' % cd, 'GT', cases[-1][1], '|', lab, cases[-1][3])
    six_cases(cases, f'{BILD}/{name}', 'GT', lab, names)

# ---- 6.5 real parts: the five GrabCAD parts of table 6.14 (input mesh + three reconstructions)
RB = [('Assem_Connecting_Rod_-_Connecting_Crank_', 'Crank'),
      ('Assem_Connecting_Rod_-_Connecting_Rod_De', 'Connecting rod'),
      ('Assem_Connecting_Rod_-_Rod_Bearing-1', 'Rod bearing bushing'),
      ('Ball_Stud_throttle', 'Throttle ball stud'),
      ('C5_Knuckle_Mesh_Decimated', 'Steering knuckle')]
_rm = {(r['method'], r['part']): r for r in json.load(open(f'{ROOT}/real_root/real_metrics.json', encoding='utf-8'))}
def _ops_str(method, part):
    o = _rm.get((method, part), {}).get('ops', '')
    return '+'.join(t[:-2] if t.endswith('x1') else t for t in o.split()) or '?'
rows = [('Input', None, GT_C), ('CAD-Recode', 'cadrecode', PR_C), ('cadrille', 'cadrille', PR_C), ('CADFit', 'cadfit', PR_C)]
fig, axes = plt.subplots(4, 5, figsize=(15, 10.2))
fig.subplots_adjust(left=0.04, right=0.99, top=0.94, bottom=0.01, wspace=0.05, hspace=0.16)
tab = {}
for j, (nme, lab) in enumerate(RB):
    for i, (rname, meth, col) in enumerate(rows):
        ax = axes[i, j]
        if meth is None:
            path, ops = f'{ROOT}/cadfit_repro/grabcad_run/{nme}.stl', None
        elif meth == 'cadfit':
            path, ops = f'{ROOT}/cadfit_repro/grabcad_run_runs/{nme}/best_greedy_parallel_iterative.py', tex_ops(_ops_str('cadfit', nme))
        else:
            path, ops = f'{ROOT}/real_root/predictions/{meth}/{nme}.py', tex_ops(_ops_str(meth, nme))
            if not os.path.isfile(f'{ROOT}/real_root/pred_stl/{meth}/{nme}.stl'):
                path, ops = None, 'invalid (not executable)'   # was not executable in the evaluation either
        panel(ax, path, col, rname)
        if ops is not None:
            tab.setdefault(lab, []).append(ops)
        if i == 0:
            ax.set_title('(%s)' % ABC[j], fontsize=10 * FS)
for i, (rname, _, _) in enumerate(rows):
    axes[i, 0].text(-0.05, 0.5, rname, rotation=90, ha='center', va='center', transform=axes[i, 0].transAxes, fontsize=10 * FS)
fig.savefig(f'{BILD}/cmp_real_qual.png', dpi=140, bbox_inches='tight'); plt.close(fig)
print('SAVED', f'{BILD}/cmp_real_qual.png')
write_table(f'{BILD}/cmp_real_qual_ops.tex', ['CAD-Recode program', 'cadrille program', 'CADFit program'],
            [('(%s) %s' % (ABC[j], lab), tab[lab]) for j, (_, lab) in enumerate(RB)], first_w=3.0, cell_ws=[3.4, 3.4, 3.4])
os.makedirs(f'{ROOT}/render_gallery/_figtmp', exist_ok=True)
json.dump(LOG, open(f'{ROOT}/render_gallery/_figtmp/step_render_log_mdt.json', 'w'), indent=1)
print('panels ok:', sum(1 for s, _ in LOG if s == 'ok'), 'invalid:', [p for s, p in LOG if s == 'invalid'])
