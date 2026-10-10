"""渲染全套肉眼对比图库 -> cadfit_repro/render_gallery/
cc_<uuid>.png   : ComplexCAD 40件, 真值(蓝) vs CADFit(橙), 标题含双方操作
real_<name>.png : 真实5件, 输入 | CADFit | CAD-Recode | cadrille 四联
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, re, glob, json
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = _ROOT
GAL = os.path.dirname(os.path.abspath(__file__))   # 图库=本目录(已升级为独立任务)
os.makedirs(GAL, exist_ok=True)
GT_C, CF_C, M1_C, M2_C = "#4C9BE8", "#E8975A", "#7BC47F", "#C79BE8"
M3_C, M4_C = "#5BBFB5", "#C9B37E"          # zero2cad / retrieval
OPS_RE = re.compile(r"\.(revolve|sweep|loft|fillet|chamfer|extrude|shell|cut|union|add|hole|cskHole)\(", re.I)


def ops_of(pyfile):
    try:
        hits = OPS_RE.findall(open(pyfile, encoding="utf-8", errors="replace").read())
    except Exception:
        return "?"
    cnt = {}
    for h in hits:
        h = h.lower()
        cnt[h] = cnt.get(h, 0) + 1
    return "+".join(f"{k}x{v}" if v > 1 else k for k, v in sorted(cnt.items())) or "none"


def draw(ax, path, color, label):
    try:
        import matplotlib.colors as mcolors
        m = trimesh.load(path, force="mesh")
        v = m.vertices - m.vertices.mean(0)
        v = v / (np.abs(v).max() + 1e-9)
        # 朗伯光照: 两盏方向光 + 环境光, 按面法线算明暗, 细节靠明暗层次而非纯色
        nrm = m.face_normals
        L1 = np.array([0.5, -0.55, 0.7]); L1 /= np.linalg.norm(L1)
        L2 = np.array([-0.7, 0.4, 0.25]); L2 /= np.linalg.norm(L2)
        inten = 0.28 + 0.62 * np.clip(nrm @ L1, 0, 1) + 0.22 * np.clip(nrm @ L2, 0, 1)
        inten = np.clip(inten, 0, 1)
        base = np.array(mcolors.to_rgb(color))
        base = 0.55 * base + 0.45 * 1.0          # 降饱和(向白偏移)
        fc = np.clip(base[None, :] * inten[:, None], 0, 1)
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


# ---- 1) ComplexCAD 40 件: GT + 5 方法, 2x3 六联 ----
PSTL = f"{ROOT}/cadfit_repro/cc_pred_stl"
done = 0
for d in sorted(glob.glob(f"{ROOT}/cadfit_repro/cc_in_runs/*/")):
    u = os.path.basename(d.rstrip("/\\"))
    gt_stl = f"{ROOT}/output/{u}/model.stl"
    cf_stl = os.path.join(d, "best_greedy_parallel_iterative.stl")
    if not os.path.isfile(cf_stl):
        cf_stl = os.path.join(d, "best_greedy_parallel.stl")
    if not (os.path.isfile(gt_stl) and os.path.isfile(cf_stl)):
        continue
    panels = [
        (gt_stl, GT_C, "GT: " + ops_of(f"{ROOT}/output/{u}/cadquery.py")),
        (cf_stl, CF_C, "CADFit: " + ops_of(cf_stl.replace(".stl", ".py"))),
        (f"{PSTL}/cadrecode/{u}.stl", M1_C,
         "CAD-Recode: " + ops_of(f"{ROOT}/predictions/cadrecode/{u}.py")),
        (f"{PSTL}/cadrille/{u}.stl", M2_C,
         "cadrille: " + ops_of(f"{ROOT}/predictions/cadrille/{u}.py")),
        (f"{PSTL}/zero2cad/{u}.stl", M3_C,
         "Zero-To-CAD: " + ops_of(f"{ROOT}/predictions/zero2cad/{u}.py")),
        (f"{PSTL}/retrieval/{u}.stl", M4_C,
         "Retrieval: " + ops_of(f"{ROOT}/predictions/retrieval/{u}.py")),
    ]
    fig = plt.figure(figsize=(13.5, 9))
    for j, (stl, col, lab) in enumerate(panels):
        ax = fig.add_subplot(2, 3, j + 1, projection="3d")
        draw(ax, stl, col, lab)
    fig.suptitle(u, fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(f"{GAL}/cc_{u[:8]}.png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    done += 1
print("ComplexCAD 对比图:", done)

# ---- 2) 真实件 5 件 x 4 方法 ----
names = [l.strip() for l in open(f"{ROOT}/real_root/names.txt") if l.strip()]
for n in names:
    fig = plt.figure(figsize=(16, 4.6))
    panels = [
        (f"{ROOT}/cadfit_repro/grabcad_run/{n}.stl", GT_C, "INPUT mesh"),
        (f"{ROOT}/cadfit_repro/grabcad_run_runs/{n}/best_greedy_parallel_iterative.stl",
         CF_C, "CADFit: " + ops_of(f"{ROOT}/cadfit_repro/grabcad_run_runs/{n}/best_greedy_parallel_iterative.py")),
        (f"{ROOT}/real_root/pred_stl/cadrecode/{n}.stl", M1_C,
         "CAD-Recode: " + ops_of(f"{ROOT}/real_root/predictions/cadrecode/{n}.py")),
        (f"{ROOT}/real_root/pred_stl/cadrille/{n}.stl", M2_C,
         "cadrille: " + ops_of(f"{ROOT}/real_root/predictions/cadrille/{n}.py")),
    ]
    for j, (stl, col, lab) in enumerate(panels):
        ax = fig.add_subplot(1, 4, j + 1, projection="3d")
        draw(ax, stl, col, lab)
    fig.suptitle(n, fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(f"{GAL}/real_{n}.png", dpi=110, bbox_inches="tight")
    plt.close(fig)
print("真实件对比图:", len(names))
print("输出目录:", GAL)
