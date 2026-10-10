# -*- coding: utf-8 -*-
"""Seeded, operation-stratified random gallery (loft panel and last panel hand-picked for visibility) and a pipeline input/output diagram.
Run with cadfit-env python (matplotlib + PIL)."""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, json, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = _ROOT; OUT = os.path.join(ROOT, 'output'); B = os.path.join(ROOT, '_rev_clone', 'bilder')
rows = {json.loads(l)['uuid']: json.loads(l) for l in open(os.path.join(ROOT, '1m_Convert', 'precision_report', 'metrics.jsonl'), encoding='utf-8')}
rng = random.Random(42)


def has(u, op): return op in [o.lower() for o in rows[u]['ops']]


ok = sorted(u for u, r in rows.items() if r['status'] == 'ok' and os.path.isfile(os.path.join(OUT, u, 'image_0.png')))
bad = sorted(u for u, r in rows.items() if r['status'] != 'ok' and os.path.isfile(os.path.join(OUT, u, 'image_0.png')))
picks = []
HAND = {'loft': 'a531a75a'}   # hand-picked: square-to-circle loft, clearly visible in the render
for op in ('loft', 'sweep', 'revolve'):
    u = rng.choice([u for u in ok if has(u, op)])          # the seeded draw is always made, so later draws stay the same
    if op in HAND:
        u = [x for x in ok if x.startswith(HAND[op])][0]
    picks.append((u, op))
picks.append((rng.choice([u for u in ok if has(u, 'fillet') and has(u, 'chamfer') and not any(has(u, o) for o in ('loft', 'sweep', 'revolve'))]), 'chamfer+fillet'))
simple = [u for u in ok if not any(has(u, o) for o in ('loft', 'sweep', 'revolve', 'chamfer', 'fillet'))]
for _ in range(3):
    picks.append((rng.choice(simple), 'sketch-extrude'))
multi = [u for u in ok if sum(has(u, o) for o in ('loft', 'sweep', 'revolve')) >= 2]   # 45 models
picks.append(([u for u in multi if u.startswith('869e90b4')][0], 'multi'))   # hand-picked: render shows both the revolve and the sweep
# contact sheet 4 x 2
W, H = 256, 256; pad = 8; lab = 34
sheet = Image.new('RGB', (4 * (W + pad) + pad, 2 * (H + lab + pad) + pad), 'white')
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype('arial.ttf', 15)
except Exception:
    font = ImageFont.load_default()
for i, (u, tag) in enumerate(picks):
    im = Image.open(os.path.join(OUT, u, 'image_0.png')).convert('RGB').resize((W, H))
    x = pad + (i % 4) * (W + pad); y = pad + (i // 4) * (H + lab + pad)
    sheet.paste(im, (x, y))
    ops = [o for o in ('loft', 'revolve', 'sweep', 'chamfer', 'fillet') if has(u, o)]
    txt = '%s | %s' % (u[:8], tag if tag == 'non-executing' else ('+'.join(ops) or 'sketch-extrude'))
    d.text((x, y + H + 4), txt, fill='black', font=font)
sheet.save(os.path.join(B, 'gallery_random.png'))
json.dump([dict(uuid=u, stratum=t, ops=[o for o in ('loft', 'revolve', 'sweep', 'chamfer', 'fillet') if has(u, o)]) for u, t in picks],
          open(os.path.join(ROOT, '_review', 'gallery_random_seed42.json'), 'w'), indent=1)
print('gallery:', [(u[:8], t) for u, t in picks])

# ---------------- pipeline diagram
fig, ax = plt.subplots(figsize=(11, 5.4)); ax.set_xlim(0, 11); ax.set_ylim(-1.1, 4.6); ax.axis('off')


def box(x, y, w, h, text, fc='#f2f2f2', ec='#333', fs=9, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08', fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal')


def arrow(x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=12, lw=1.1, color='#333'))


box(0.2, 1.7, 2.1, 1.2, 'Zero-To-CAD\nCadQuery program\n(inherited)', fc='#e8e8e8', bold=True)
box(2.9, 1.7, 2.3, 1.2, 'curate + execute\nCadQuery / OCP 7.8\n(this thesis)', fc='#dbe9f6', bold=True)
arrow(2.3, 2.3, 2.9, 2.3)
outs = [('point cloud + normals\n(8192 pts, PLY/NPY)', 'generated'), ('B-rep export\n(kernel-native)', 'derived'),
        ('geometry metadata\n(counts, bbox, latency)', 'derived'), ('text description\n(structured + free)', 'derived / heuristic'),
        ('engineering drawing\n(DXF/SVG/PNG, ISO-inspired)', 'generated'), ('assemblies\n(single / two-part, mates)', 'generated')]
y = 4.1
for i, (t, prov) in enumerate(outs):
    yy = 4.05 - i * 0.68
    box(6.0, yy - 0.25, 2.9, 0.55, t, fs=8)
    ax.text(9.05, yy + 0.02, prov, fontsize=8, va='center', color='#555')
    arrow(5.2, 2.3, 6.0, yy + 0.02)
box(0.2, -1.0, 10.5, 0.7, 'quality checks (Ch. 5, Sec. 4.7, Sec. 4.8): L1 execution / validity / entity-count agreement  -  L2 parameter-to-STEP round-trip and feature measurers'
    + chr(10) + 'L3 operation coverage and co-occurrence  -  drawing rule audit (ISO 129-1 / 3098 / 5455 / 5456-2)  -  mate-constraint replay of every assembly', fc='#fff4d6', fs=7.2)
ax.text(0.2, 0.55, 'inherited: programs, 8 rendered views, STL/STEP', fontsize=8, color='#555')
ax.text(0.2, 0.25, 'not delivered: sketch constraints, depth/normal/edge maps, tolerance annotation', fontsize=8, color='#555')
fig.savefig(os.path.join(B, 'pipeline_overview.png'), dpi=200, bbox_inches='tight')
print('diagram written')
