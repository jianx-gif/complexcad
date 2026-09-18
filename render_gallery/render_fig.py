"""渲染 CADFit 定性图: 3个复杂件(revolve/sweep/loft), 真值(上) vs CADFit重建(下)。"""
import numpy as np, trimesh
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = "E:/3005/data"
RUNS = f"{ROOT}/cadfit_repro/cc_in_runs"
OUT = f"{ROOT}/overleaf_thesis/bilder/cmp_cadfit_qual.png"

# (uuid, GT操作标签, CADFit操作标签)
CASES = [
    ("071a220d-5b4e-fc1d-c9ce-3a3a3b23b0ab", "revolve + fillet + chamfer", "extrude + union"),
    ("31d4bb86-0545-3475-30fa-96ba18d87b54", "sweep + fillet + chamfer",   "extrude + union"),
    ("243ce854-9883-1843-c49b-d55366badb0c", "loft",                        "extrude + union"),
]
GT_C, CF_C = "#4C9BE8", "#E8975A"


def draw(ax, path, color):
    m = trimesh.load(path, force="mesh")
    v = m.vertices - m.vertices.mean(0); v = v / (np.abs(v).max() + 1e-9)
    ax.add_collection3d(Poly3DCollection(v[m.faces], facecolor=color,
                        edgecolor=(0, 0, 0, 0.10), linewidths=0.15))
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=24, azim=-55)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_visible(False)


fig = plt.figure(figsize=(12, 8))
for j, (u, gtlab, cflab) in enumerate(CASES):
    ax = fig.add_subplot(2, 3, j + 1, projection="3d")
    draw(ax, f"{ROOT}/output/{u}/model.stl", GT_C)
    ax.set_title(f"GT: {gtlab}", fontsize=11)
    ax2 = fig.add_subplot(2, 3, j + 4, projection="3d")
    draw(ax2, f"{RUNS}/{u}/best_greedy_parallel_iterative.stl", CF_C)
    ax2.set_title(f"CADFit: {cflab}", fontsize=11)
fig.text(0.5, 0.955, "Ground truth (top) vs. CADFit reconstruction (bottom)",
         ha="center", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(OUT, dpi=140, bbox_inches="tight")
print("SAVED", OUT)
