# -*- coding: utf-8 -*-
"""Figure 4.7 (fig:asm-trio): body A, body B and the assembled two-part assembly, rendered from
STEP with the B-rep renderer of render_step.py (same muted palette as Figures 6.1-6.5).
Usage: python render_fig47_trio.py <assembly model.step>  (run with cadfit-env python)"""
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_step as R

ROOT = 'E:/3005/data/'
A = ROOT + 'output/b4003ad7-357f-6eda-915f-c7e625bb939f/model.step'
B = ROOT + 'output/5d97e290-a077-580a-60a3-f23349f63e46/model.step'
ASM = sys.argv[1]
OUT = ROOT + '_rev_clone/bilder/assembly_example_trio.png'
COLOR = '#c8a25a'          # sand, as the prediction panels of Chapter 6

fig, axes = plt.subplots(1, 3, figsize=(12, 4.3))
for ax, path, title in zip(axes, (A, B, ASM), ('(a) Body A', '(b) Body B', '(c) Assembly (A + B + fasteners)')):
    ax.set_axis_off()
    img = R.render(path, COLOR, size=1000)
    if img is None:
        sys.exit('render failed: ' + path)
    ax.imshow(R.crop(img), interpolation='lanczos')
    ax.set_title(title, fontsize=11)
fig.tight_layout()
fig.savefig(OUT, dpi=150, bbox_inches='tight'); plt.close(fig)
print('SAVED', OUT)
