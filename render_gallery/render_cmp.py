"""渲染 真值STL vs CADFit重建STL 的并排对比图(headless, matplotlib)。"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import sys, numpy as np, trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

U = "31d4bb86-0545-3475-30fa-96ba18d87b54"
GT = f"{_ROOT}/output/{U}/model.stl"
PR = f"{_ROOT}/cadfit_repro/test_one_runs/{U}/best_greedy_parallel.stl"
OUT = _ROOT + '/render_gallery/compare_31d4bb86.png'


def draw(ax, path, title, color):
    m = trimesh.load(path, force="mesh")
    v = m.vertices - m.vertices.mean(0)
    s = np.abs(v).max()
    v = v / s
    tris = v[m.faces]
    pc = Poly3DCollection(tris, alpha=1.0, facecolor=color, edgecolor=(0, 0, 0, 0.08), linewidths=0.2)
    ax.add_collection3d(pc)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=22, azim=-58)
    ax.set_title(title, fontsize=13)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane.pane.set_visible(False)


fig = plt.figure(figsize=(12, 5.5))
ax1 = fig.add_subplot(121, projection="3d")
draw(ax1, GT, "INPUT: mesh (STL, triangles only)", "#4C9BE8")
ax2 = fig.add_subplot(122, projection="3d")
draw(ax2, PR, "OUTPUT: CADFit rebuild = 2 extrudes (IoU 0.973)", "#E8975A")
fig.suptitle("CADFit: input is a raw mesh -> output CadQuery; geometry matched, operations wrong", fontsize=13, y=0.97)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(OUT, dpi=130, bbox_inches="tight")
print("SAVED", OUT)
