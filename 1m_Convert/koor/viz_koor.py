"""可视化对比: ORIG vs CONVERTED 几何, 归一化视角看形状差异。
matplotlib + cadquery tessellate, 无头渲染。"""
import sys, os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery as cq
from types import SimpleNamespace
import math


def mesh_of(src):
    g = {"cq": cq, "SimpleNamespace": SimpleNamespace, "math": math, "__name__": "x"}
    exec(src, g)
    r = g.get("result")
    if r is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                r = v
    shape = r.val() if hasattr(r, "val") else r
    bb = shape.BoundingBox()
    tol = max(bb.xlen, bb.ylen, bb.zlen) / 200.0
    verts, tris = shape.tessellate(tol)
    V = np.array([[p.x, p.y, p.z] for p in verts])
    F = np.array(tris)
    return V, F


def norm(V):
    c = (V.max(0) + V.min(0)) / 2
    V = V - c
    s = np.abs(V).max()
    return V / (s if s > 0 else 1)


def draw(ax, V, F, title, color):
    V = norm(V)
    polys = V[F]
    pc = Poly3DCollection(polys, alpha=1.0, facecolor=color,
                          edgecolor=(0, 0, 0, 0.15), linewidths=0.2)
    ax.add_collection3d(pc)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=-50)
    ax.set_title(title, fontsize=11)
    ax.set_axis_off()


def main():
    # args: list of (label, orig_code, scaled_code) via json file path
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    n = len(spec)
    fig = plt.figure(figsize=(8, 4 * n))
    for i, item in enumerate(spec):
        Vo, Fo = mesh_of(item["orig"])
        Vs, Fs = mesh_of(item["scaled"])
        ax1 = fig.add_subplot(n, 2, 2 * i + 1, projection="3d")
        draw(ax1, Vo, Fo, f"{item['label']}  ORIG", "#4c78a8")
        ax2 = fig.add_subplot(n, 2, 2 * i + 2, projection="3d")
        draw(ax2, Vs, Fs, f"{item['label']}  CONVERTED", "#a67b4c")
    plt.tight_layout()
    fig.savefig(out, dpi=110, bbox_inches="tight")
    print("saved", out)


if __name__ == "__main__":
    main()
