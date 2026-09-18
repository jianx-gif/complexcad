"""重渲 4 张论文定性图(带朗伯光照) -> overleaf_thesis/bilder/
A cmp_cadfit_qual : 3件 GT vs CADFit (原件不变)
B cmp_real_qual   : 3真实件 输入 vs CADFit (原件不变)
C cmp_cadrecode_qual: 3件 GT vs CAD-Recode (按原型重选, 打印CD/操作供图注)
D cmp_retrieval_qual: 3件 GT vs 检索     (同上)
"""
import os, re, glob, json, subprocess
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = "E:/3005/data"
BILD = f"{ROOT}/overleaf_thesis/bilder"
TMP = f"{ROOT}/render_gallery/_figtmp"
os.makedirs(TMP, exist_ok=True)
GT_C, PR_C = "#4C9BE8", "#E8975A"
OPS_RE = re.compile(r"\.(revolve|sweep|loft|fillet|chamfer|extrude|shell|cut|union|add|hole|cskHole)\(", re.I)


def ops_of(pyfile):
    try:
        hits = OPS_RE.findall(open(pyfile, encoding="utf-8", errors="replace").read())
    except Exception:
        return {}
    cnt = {}
    for h in hits:
        h = h.lower()
        cnt[h] = cnt.get(h, 0) + 1
    return cnt


def fmt(cnt):
    return "+".join(f"{k}x{v}" if v > 1 else k for k, v in sorted(cnt.items())) or "none"


def wrap_ops(label, width=26):
    """长操作串按 '+' 折行, 每行不超 width 字符, 防止相邻面板标题重叠。"""
    if len(label) <= width:
        return label
    head, sep, ops = label.partition(": ")
    parts = ops.split("+") if sep else label.split("+")
    lines, cur = [], (head + ": " if sep else "")
    for i, p in enumerate(parts):
        tok = p if not cur or cur.endswith(": ") else "+" + p
        if cur and not cur.endswith(": ") and len(cur) + len(tok) > width:
            lines.append(cur + "+")
            cur = p
        else:
            cur += tok
    lines.append(cur)
    return "\n".join(lines)


def draw(ax, path, color, label):
    m = trimesh.load(path, force="mesh")
    v = m.vertices - m.vertices.mean(0)
    v = v / (np.abs(v).max() + 1e-9)
    nrm = m.face_normals
    L1 = np.array([0.5, -0.55, 0.7]); L1 /= np.linalg.norm(L1)
    L2 = np.array([-0.7, 0.4, 0.25]); L2 /= np.linalg.norm(L2)
    inten = np.clip(0.28 + 0.62 * np.clip(nrm @ L1, 0, 1)
                    + 0.22 * np.clip(nrm @ L2, 0, 1), 0, 1)
    base = np.array(mcolors.to_rgb(color))
    base = 0.55 * base + 0.45 * 1.0
    fc = np.clip(base[None, :] * inten[:, None], 0, 1)
    ax.add_collection3d(Poly3DCollection(v[m.faces], facecolors=fc,
                        edgecolor=(0, 0, 0, 0.18), linewidths=0.15))
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=22, azim=-60)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_visible(False)
    ax.set_title(wrap_ops(label), fontsize=8.5)


def two_rows(cases, out, top_lab, bot_lab):
    """cases: [(top_stl, top_ops, bot_stl, bot_ops, subtitle)]"""
    fig = plt.figure(figsize=(12, 8))
    for j, (ts, to, bs, bo, sub) in enumerate(cases):
        ax = fig.add_subplot(2, 3, j + 1, projection="3d")
        draw(ax, ts, GT_C, f"{top_lab}: {to}")
        ax.text2D(0.5, 1.26, sub, ha="center", transform=ax.transAxes, fontsize=9)
        ax2 = fig.add_subplot(2, 3, j + 4, projection="3d")
        draw(ax2, bs, PR_C, f"{bot_lab}: {bo}")
    fig.tight_layout()
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print("SAVED", out)


def full_uuid(prefix, meth):
    g = glob.glob(f"{ROOT}/predictions/{meth}/{prefix}*.py")
    return os.path.basename(g[0])[:-3] if g else None


def exec_pred(pyfile, out_stl):
    if os.path.isfile(out_stl):
        return True
    r = subprocess.run(["python", "-X", "utf8", f"{ROOT}/real_root/exec_pred.py",
                        pyfile, out_stl], capture_output=True, timeout=90)
    return r.returncode == 0 and os.path.isfile(out_stl)


def build_fig(meth, prefixes, out_png, bot_lab):
    metrics = {json.loads(l)["uuid"]: json.loads(l) for l in
               open(f"{ROOT}/1m_Convert/precision_report/pred_metrics_{meth}.jsonl",
                    encoding="utf-8")}
    cases = []
    for p in prefixes:
        if len(cases) >= 3:
            break
        u = full_uuid(p, meth)
        if not u:
            continue
        pred_py = f"{ROOT}/predictions/{meth}/{u}.py"
        pred_stl = f"{TMP}/{meth}_{u[:8]}.stl"
        if not exec_pred(pred_py, pred_stl):
            print("  exec-fail", u[:8]); continue
        gt_ops = ops_of(f"{ROOT}/output/{u}/cadquery.py")
        pr_ops = ops_of(pred_py)
        cd = metrics.get(u, {}).get("chamfer")
        cases.append((f"{ROOT}/output/{u}/model.stl", fmt(gt_ops),
                      pred_stl, fmt(pr_ops),
                      "%s  CD=%.3f" % (u[:8], cd if cd is not None else -1)))
        print("CASE", meth, u[:8], "CD=%.3f" % (cd or -1),
              "| GT:", fmt(gt_ops), "| PRED:", fmt(pr_ops))
    two_rows(cases, out_png, "GT", bot_lab)


# A: CADFit 3件(原件)
CF = [("071a220d-5b4e-fc1d-c9ce-3a3a3b23b0ab", "revolve + fillet + chamfer"),
      ("31d4bb86-0545-3475-30fa-96ba18d87b54", "sweep + fillet + chamfer"),
      ("243ce854-9883-1843-c49b-d55366badb0c", "loft")]
cases = []
for u, lab in CF:
    d = f"{ROOT}/cadfit_repro/cc_in_runs/{u}"
    cases.append((f"{ROOT}/output/{u}/model.stl",
                  fmt(ops_of(f"{ROOT}/output/{u}/cadquery.py")),
                  f"{d}/best_greedy_parallel_iterative.stl",
                  fmt(ops_of(f"{d}/best_greedy_parallel_iterative.py")), lab))
two_rows(cases, f"{BILD}/cmp_cadfit_qual.png", "GT", "CADFit")

# B: 真实件3件 × 全部方法(输入/CAD-Recode/cadrille/CADFit)。学习法 EXEC-FAIL 的
# 面板留空标 invalid —— 正是正文观察一(有效性分野)的可视化。
RB = [("Ball_Stud_throttle", "Ball stud (turned part)"),
      ("Assem_Connecting_Rod_-_Rod_Bearing-1", "Rod bearing bushing"),
      ("C5_Knuckle_Mesh_Decimated", "Steering knuckle")]
_rm = {(r["method"], r["part"]): r for r in
       json.load(open(f"{ROOT}/real_root/real_metrics.json", encoding="utf-8"))}


def _ops_str(method, part):
    o = _rm.get((method, part), {}).get("ops", "")
    return "+".join(t[:-2] if t.endswith("x1") else t for t in o.split()) or "?"


fig = plt.figure(figsize=(12, 15))
rows = [("Input", None, GT_C), ("CAD-Recode", "cadrecode", PR_C),
        ("cadrille", "cadrille", PR_C), ("CADFit", "cadfit", PR_C)]
for j, (n, lab) in enumerate(RB):
    for i, (rname, meth, col) in enumerate(rows):
        ax = fig.add_subplot(4, 3, i * 3 + j + 1, projection="3d")
        if meth is None:
            stl, title = f"{ROOT}/cadfit_repro/grabcad_run/{n}.stl", "Input mesh"
        elif meth == "cadfit":
            stl = f"{ROOT}/cadfit_repro/grabcad_run_runs/{n}/best_greedy_parallel_iterative.stl"
            title = f"CADFit: {_ops_str('cadfit', n)}"
        else:
            stl = f"{ROOT}/real_root/pred_stl/{meth}/{n}.stl"
            title = f"{rname}: {_ops_str(meth, n)}"
        if meth and not os.path.isfile(stl):
            ax.set_axis_off()
            ax.text2D(0.5, 0.5, f"{rname}\ninvalid\n(not executable)",
                      ha="center", va="center", transform=ax.transAxes,
                      fontsize=10, color="#993333")
        else:
            draw(ax, stl, col, title)
        if i == 0:
            ax.text2D(0.5, 1.22, lab, ha="center", transform=ax.transAxes,
                      fontsize=10, weight="bold")
fig.tight_layout()
fig.savefig(f"{BILD}/cmp_real_qual.png", dpi=140, bbox_inches="tight")
plt.close(fig)
print("SAVED", f"{BILD}/cmp_real_qual.png")

# C: CAD-Recode (按原型: 倒角件 / 旋转+圆角 / 多特征)
build_fig("cadrecode", ["77609f32", "a1d1c4c1", "0afda985", "c50da0b7", "925bbf47"],
          f"{BILD}/cmp_cadrecode_qual.png", "CAD-Recode")

# D: 检索 (revolve+fillet / loft / revolve多特征)
build_fig("retrieval", ["a1d1c4c1", "fef3922d", "6a8c9b4a", "7049af79", "20f7c650"],
          f"{BILD}/cmp_retrieval_qual.png", "Retrieved")
print("ALL FIGS DONE")
