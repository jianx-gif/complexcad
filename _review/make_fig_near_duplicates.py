# -*- coding: utf-8 -*-
"""Figure for annotation #66: three quarantined near-duplicate pairs (test model next to the
quarantined model), chosen deterministically as the pairs with the smallest normalised
Chamfer distance, rendered from the upstream image_0.png of each model."""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

R = _ROOT
pairs = json.load(open(os.path.join(R, 'splits', 'quarantine_pairs.json'), encoding='utf-8'))
ranked = sorted(pairs.items(), key=lambda kv: kv[1]['chamfer'])
chosen, seen = [], set()
for q, rec in ranked:
    if rec['test_uuid'] in seen:
        continue
    chosen.append((rec['test_uuid'], q, rec['cosine'], rec['chamfer'])); seen.add(rec['test_uuid'])
    if len(chosen) == 3:
        break
fig, ax = plt.subplots(2, 3, figsize=(9, 5.6))
for j, (t, q, cos, cd) in enumerate(chosen):
    for i, (u, lab) in enumerate(((t, 'test'), (q, 'quarantined'))):
        ax[i, j].imshow(Image.open(os.path.join(R, 'output', u, 'image_0.png')).convert('RGB'))
        ax[i, j].set_axis_off()
        ax[i, j].set_title('%s %s' % (lab, u[:8]), fontsize=9)
    ax[1, j].text(0.5, -0.08, 'cosine %.3f, CD %.4f' % (cos, cd), transform=ax[1, j].transAxes,
                  ha='center', va='top', fontsize=9)
fig.tight_layout()
out = os.path.join(R, '_rev_clone', 'bilder', 'near_duplicates.png')
fig.savefig(out, dpi=150, bbox_inches='tight')
print('saved', out)
for c in chosen:
    print(c)
