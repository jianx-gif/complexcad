"""装配对比图: asm_<name>.png 四联 = GT装配 | CADFit | CAD-Recode | cadrille"""
import os, re
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = "E:/3005/data"
ASM = f"{ROOT}/asm_repro"
GAL = os.path.dirname(os.path.abspath(__file__))
GT_C, CF_C, M1_C, M2_C = "#4C9BE8", "#E8975A", "#7BC47F", "#C79BE8"
OPS_RE = re.compile(r"\.(revolve|sweep|loft|fillet|chamfer|extrude|shell|cut|union|add|hole|cskHole)\(", re.I)


def ops_of(py):
    try:
        h = OPS_RE.findall(open(py, encoding="utf-8", errors="replace").read())
    except Exception:
        return "?"
    c = {}
    for x in h:
        x = x.lower(); c[x] = c.get(x, 0) + 1
    return "+".join(f"{k}x{v}" if v > 1 else k for k, v in sorted(c.items())) or "none"


def draw(ax, path, color, label):
    try:
        m = trimesh.load(path, force="mesh")
        v = m.vertices - m.vertices.mean(0)
        v = v / (np.abs(v).max() + 1e-9)
        nrm = m.face_normals
        L1 = np.array([0.5, -0.55, 0.7]); L1 /= np.linalg.norm(L1)
        L2 = np.array([-0.7, 0.4, 0.25]); L2 /= np.linalg.norm(L2)
        it = np.clip(0.28 + 0.62 * np.clip(nrm @ L1, 0, 1)
                     + 0.22 * np.clip(nrm @ L2, 0, 1), 0, 1)
        base = np.array(mcolors.to_rgb(color)); base = 0.55 * base + 0.45
        fc = np.clip(base[None, :] * it[:, None], 0, 1)
        ax.add_collection3d(Poly3DCollection(v[m.faces], facecolors=fc,
                            edgecolor=(0, 0, 0, 0.18), linewidths=0.15))
    except Exception:
        ax.text2D(0.5, 0.5, "invalid", ha="center", va="center",
                  transform=ax.transAxes, fontsize=14, color="#B33")
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=22, azim=-60)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_visible(False)
    ax.set_title(label, fontsize=10)


names = [l.strip() for l in open(f"{ASM}/names.txt") if l.strip()]
for n in names:
    fig = plt.figure(figsize=(16, 4.6))
    panels = [
        (f"{ASM}/asm_in/{n}.stl", GT_C, "GT assembly (multi-body)"),
        (f"{ASM}/asm_fit_in_runs/{n}/best_greedy_parallel_iterative.stl", CF_C,
         "CADFit: " + ops_of(f"{ASM}/asm_fit_in_runs/{n}/best_greedy_parallel_iterative.py")),
        (f"{ASM}/pred_stl/cadrecode/{n}.stl", M1_C,
         "CAD-Recode: " + ops_of(f"{ASM}/predictions/cadrecode/{n}.py")),
        (f"{ASM}/pred_stl/cadrille/{n}.stl", M2_C,
         "cadrille: " + ops_of(f"{ASM}/predictions/cadrille/{n}.py")),
    ]
    for j, (stl, col, lab) in enumerate(panels):
        ax = fig.add_subplot(1, 4, j + 1, projection="3d")
        draw(ax, stl, col, lab)
    fig.suptitle(n, fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(f"{GAL}/asm_{n}.png", dpi=110, bbox_inches="tight")
    plt.close(fig)
print("装配对比图:", len(names))
