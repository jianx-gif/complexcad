"""
为分布决策生成直观可视化图表（图内标识为英文）。
读 out/*.json，输出 out/dist_*.png
用法: python make_distribution_charts.py
"""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 中文字体（Windows 自带黑体）
for fp in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
        plt.rcParams["font.family"] = fm.FontProperties(fname=fp).get_name()
        break
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "out")
def load(n):
    p = os.path.join(OUT, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
z = load("zero_to_cad_test_stats.json")
fu = load("fusion360_recon_stats.json")
dc = load("deepcad_test_stats.json")
cr = load("cadrecode_v15_train_stats.json")  # v1.5 train 全量 981,865 条

C = {"ztc": "#2c7fb8", "fu": "#41ab5d", "dc": "#969696", "cr": "#d95f0e"}

# ========== 图1: 四数据集操作覆盖率分组柱状 ==========
OPS = ["Extrude", "Revolve", "Loft", "Sweep", "Chamfer", "Fillet"]
KEY = ["extrude", "revolve", "loft", "sweep", "chamfer", "fillet"]
def gp(stats, key="operation_presence_pct"):
    d = (stats or {}).get(key, {}); return [d.get(k, 0) for k in KEY]
ztc = gp(z)
crd = gp(cr, "complex_ops_coverage_pct"); crd[0] = (cr or {}).get("operation_presence_pct", {}).get("extrude", 0)
dcd = [100] + [(dc or {}).get("complex_ops_coverage_pct", {}).get(k, 0) for k in KEY[1:]]
fud = [100, 0, 0, 0, 0, 0]
mat = np.array([ztc, fud, dcd, crd]); names = ["Zero-To-CAD", "Fusion360", "DeepCAD", "CAD-Recode"]
cols = [C["ztc"], C["fu"], C["dc"], C["cr"]]
x = np.arange(len(OPS)); w = 0.2
fig, ax = plt.subplots(figsize=(12, 6))
for i in range(4):
    b = ax.bar(x + (i-1.5)*w, mat[i], w, label=names[i], color=cols[i])
    for j, v in enumerate(mat[i]):
        if v > 0: ax.text(x[j]+(i-1.5)*w, v+1, f"{v:.0f}", ha="center", va="bottom", fontsize=7)
ax.set_xticks(x); ax.set_xticklabels(OPS, fontsize=11)
ax.set_ylabel("Model coverage (%)", fontsize=12)
ax.set_title("Modeling operation coverage across four CAD datasets", fontsize=14, fontweight="bold")
ax.legend(fontsize=10); ax.grid(axis="y", alpha=0.3); ax.set_ylim(0, 108)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "dist_1_operation_coverage.png"), dpi=150); plt.close()
print("[+] dist_1_operation_coverage.png")

# ========== 图2: Zero-To-CAD 复杂操作绝对样本数（最关键的决策图） ==========
comp = ["Chamfer", "Fillet", "Revolve", "Sweep", "Loft"]
ckey = ["chamfer", "fillet", "revolve", "sweep", "loft"]
cnt = [(z or {}).get("operation_presence_count", {}).get(k, 0) for k in ckey]
fig, ax = plt.subplots(figsize=(10, 5.5))
barcolors = ["#74a9cf", "#74a9cf", "#74a9cf", "#e34a33", "#e34a33"]  # 红色高亮稀缺的
bars = ax.bar(comp, cnt, color=barcolors)
for b, v in zip(bars, cnt):
    ax.text(b.get_x()+b.get_width()/2, v+80, str(v), ha="center", fontsize=11, fontweight="bold")
ax.axhline(2500, ls="--", color="gray", alpha=0.7)
ax.text(4.3, 2600, "Suggested minimum for evaluation ~2500", color="gray", fontsize=9, ha="right")
ax.set_ylabel("# models (out of 10,000)", fontsize=12)
ax.set_title("Zero-To-CAD complex-operation sample counts: Sweep/Loft under-represented (red)", fontsize=13, fontweight="bold")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "dist_2_ztc_complex_count.png"), dpi=150); plt.close()
print("[+] dist_2_ztc_complex_count.png")

# ========== 图3: 草图图元覆盖率对比（含样条短板） ==========
PRIM = ["Line", "Circle", "Arc", "Rect", "Spline", "Polygon"]
pk = ["line", "circle", "arc", "rect", "spline", "polygon"]
def gprim(s, key="sketch_primitive_presence_pct"):
    d = (s or {}).get(key, {}); return [d.get(k, 0) for k in pk]
zp = gprim(z)
fp_ = gprim(fu, "sketch_curve_presence_pct")
dp = gprim(dc)
cp = gprim(cr)   # CAD-Recode v1.5 train：line=segment，spline/polygon 词表不含=0
x = np.arange(len(PRIM)); w = 0.2
fig, ax = plt.subplots(figsize=(12, 5.5))
for i, (d, nm, c) in enumerate([(zp, "Zero-To-CAD", C["ztc"]), (fp_, "Fusion360", C["fu"]),
                                (dp, "DeepCAD", C["dc"]), (cp, "CAD-Recode", C["cr"])]):
    ax.bar(x+(i-1.5)*w, d, w, label=nm, color=c)
    for j, v in enumerate(d):
        if v > 0: ax.text(x[j]+(i-1.5)*w, v+1, f"{v:.0f}", ha="center", va="bottom", fontsize=7)
ax.set_xticks(x); ax.set_xticklabels(PRIM, fontsize=11)
ax.set_ylabel("Model coverage (%)", fontsize=12)
ax.set_title("Sketch primitive coverage across four CAD datasets", fontsize=13, fontweight="bold")
ax.legend(); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "dist_3_primitives.png"), dpi=150); plt.close()
print("[+] dist_3_primitives.png")

# ========== 图4: 序列长度/复杂度对比 ==========
# CAD-Recode 口径与 DeepCAD 对齐：草图图元(segment/arc/circle/rect) + 建模操作(extrude/cylinder/box/union) 计数
means = [(z or {}).get("ops_count_stats", {}).get("mean", 0),
         (fu or {}).get("sequence_length_stats", {}).get("mean", 0),
         (dc or {}).get("sequence_length_stats", {}).get("mean", 0),
         (cr or {}).get("sequence_length_stats", {}).get("mean", 0)]
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(["Zero-To-CAD", "Fusion360", "DeepCAD", "CAD-Recode"], means,
              color=[C["ztc"], C["fu"], C["dc"], C["cr"]])
for b, v in zip(bars, means):
    ax.text(b.get_x()+b.get_width()/2, v+0.3, f"{v:.1f}", ha="center", fontsize=12, fontweight="bold")
ax.set_ylabel("Mean operations / commands per model", fontsize=12)
ax.set_title("Model complexity: Zero-To-CAD highest, DeepCAD / CAD-Recode simplest", fontsize=13, fontweight="bold")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "dist_4_complexity.png"), dpi=150); plt.close()
print("[+] dist_4_complexity.png")

# ========== 图5: Zero-To-CAD 操作数分布直方图（你的基底形状） ==========
if z and z.get("ops_count_distribution"):
    d = {int(k): v for k, v in z["ops_count_distribution"].items()}
    ks = sorted(d); vs = [d[k] for k in ks]
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(ks, vs, color=C["ztc"], width=0.9)
    m = z["ops_count_stats"]["mean"]
    ax.axvline(m, color="red", ls="--", label=f"mean = {m}")
    ax.set_xlabel("Operations per model", fontsize=12); ax.set_ylabel("# models", fontsize=12)
    ax.set_title("Zero-To-CAD: distribution of operations per model (peak at 20-26)", fontsize=13, fontweight="bold")
    ax.legend(); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "dist_5_ztc_opscount_hist.png"), dpi=150); plt.close()
    print("[+] dist_5_ztc_opscount_hist.png")

# ========== 图6: Zero-To-CAD 全操作分布（饼+柱混合用横向柱） ==========
if z:
    pres = z["operation_presence_pct"]
    items = sorted(pres.items(), key=lambda kv: kv[1])
    labels = [k for k, _ in items]; vals = [v for _, v in items]
    fig, ax = plt.subplots(figsize=(9, 6))
    colors = ["#e34a33" if k in ("sweep", "loft") else "#74a9cf" for k in labels]
    ax.barh(labels, vals, color=colors)
    for i, v in enumerate(vals):
        ax.text(v+0.5, i, f"{v:.1f}%", va="center", fontsize=9)
    ax.set_xlabel("Model coverage (%)", fontsize=12)
    ax.set_title("Zero-To-CAD: full operation distribution (Sweep/Loft lowest, red)", fontsize=13, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "dist_6_ztc_all_ops.png"), dpi=150); plt.close()
    print("[+] dist_6_ztc_all_ops.png")

print("\n全部分布图已写入", OUT)
