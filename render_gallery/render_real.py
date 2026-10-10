"""真实件定性图: 输入网格(上) vs CADFit重建(下), 3例。"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import numpy as np, trimesh
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = _ROOT + '/cadfit_repro'
OUT = _ROOT + '/overleaf_thesis/bilder/cmp_real_qual.png'

CASES = [
    ("Ball_Stud_throttle", "Ball stud (turned part)", "IoU 0.80, extrude + union"),
    ("Assem_Connecting_Rod_-_Rod_Bearing-1", "Rod bearing bushing", "IoU 0.98, extrude + union"),
    ("C5_Knuckle_Mesh_Decimated", "Steering knuckle", "IoU 0.69, extrudes + Booleans"),
]
GT_C, CF_C = "#4C9BE8", "#E8975A"


def draw(ax, path, color):
    m = trimesh.load(path, force="mesh")
    v = m.vertices - m.vertices.mean(0); v = v / (np.abs(v).max() + 1e-9)
    ax.add_collection3d(Poly3DCollection(v[m.faces], facecolor=color,
                        edgecolor=(0, 0, 0, 0.08), linewidths=0.12))
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=22, azim=-60)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_visible(False)


fig = plt.figure(figsize=(12, 8))
for j, (n, title, sub) in enumerate(CASES):
    ax = fig.add_subplot(2, 3, j + 1, projection="3d")
    draw(ax, f"{HERE}/grabcad_run/{n}.stl", GT_C)
    ax.set_title(f"Real part: {title}", fontsize=11)
    ax2 = fig.add_subplot(2, 3, j + 4, projection="3d")
    draw(ax2, f"{HERE}/grabcad_run_runs/{n}/best_greedy_parallel_iterative.stl", CF_C)
    ax2.set_title(f"CADFit: {sub}", fontsize=11)
fig.text(0.5, 0.955, "Real-world meshes (top) vs. CADFit reconstruction (bottom)",
         ha="center", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(OUT, dpi=140, bbox_inches="tight")
print("SAVED", OUT)
