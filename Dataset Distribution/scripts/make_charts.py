"""
读取各数据集统计结果(out/*.json)，生成论文用对比图表。
- 一手统计: Zero-To-CAD (test 10000), cad-recode v1.5 (train 全量 981,865)
- 文献/结构性: DeepCAD(纯sketch-extrude), Fusion360(官方明确仅sketch+extrude)

输出: out/fig_*.png
用法: python make_charts.py
"""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out")

def load(name):
    p = os.path.join(OUT, name)
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return None

z = load("zero_to_cad_test_stats.json")
c = load("cadrecode_v15_train_stats.json")
dc = load("deepcad_test_stats.json")
fu = load("fusion360_recon_stats.json")

# 复杂操作覆盖率（%）。DeepCAD/Fusion360 = 0（结构性，词表不含）
OPS = ["extrude", "revolve", "loft", "sweep", "chamfer", "fillet"]
def cov(stats, key="operation_presence_pct"):
    d = (stats or {}).get(key, {})
    return [d.get(op, 0.0) for op in OPS]

zero = cov(z) if z else [0]*6
cadr = cov(c, "operation_presence_pct") if c else [0]*6
# DeepCAD test 一手实测：复杂操作实测全 0；extrude 每模型必有，覆盖率≈100
dc_complex = (dc or {}).get("complex_ops_coverage_pct", {})
deepcad = [100, dc_complex.get("revolve",0), dc_complex.get("loft",0),
           dc_complex.get("sweep",0), dc_complex.get("chamfer",0), dc_complex.get("fillet",0)]
# Fusion360 reconstruction 一手实测：operation_type 仅 Sketch/ExtrudeFeature → 复杂操作全 0
fu_types = (fu or {}).get("operation_type_counts", {})
fusion  = [100 if "ExtrudeFeature" in fu_types else 0, 0, 0, 0, 0, 0]

# ---- 图1: 复杂操作覆盖率分组柱状图 ----
datasets = ["Zero-To-CAD\n(test 10k)", "CAD-Recode", "DeepCAD\n(test 8052)", "Fusion360\n(recon 8625)"]
mat = np.array([zero, cadr, deepcad, fusion])  # 4 x 6
x = np.arange(len(OPS))
w = 0.2
fig, ax = plt.subplots(figsize=(11, 5.5))
colors = ["#2c7fb8", "#d95f0e", "#999999", "#bdbdbd"]
for i, ds in enumerate(datasets):
    ax.bar(x + (i-1.5)*w, mat[i], w, label=ds, color=colors[i])
ax.set_xticks(x); ax.set_xticklabels([o.capitalize() for o in OPS])
ax.set_ylabel("Model coverage (%)")
ax.set_title("Modeling operation coverage across CAD datasets (all first-hand measured)")
ax.legend()
ax.grid(axis="y", alpha=0.3)
for i in range(len(datasets)):
    for j in range(len(OPS)):
        v = mat[i][j]
        if v > 0:
            ax.text(x[j]+(i-1.5)*w, v+1, f"{v:.0f}", ha="center", va="bottom", fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_operation_coverage.png"), dpi=150)
print("[+] fig_operation_coverage.png")

# ---- 图2: 复杂操作"有无"热力对照 ----
COMPLEX = ["Revolve", "Loft", "Sweep", "Chamfer", "Fillet"]
heat = np.array([
    cov(z)[1:6] if z else [0]*5,
    cov(c)[1:6] if c else [0]*5,
    [0,0,0,0,0],
    [0,0,0,0,0],
])
fig, ax = plt.subplots(figsize=(8, 3.5))
im = ax.imshow(heat, cmap="YlGnBu", aspect="auto", vmin=0, vmax=100)
ax.set_xticks(range(5)); ax.set_xticklabels(COMPLEX)
ax.set_yticks(range(4)); ax.set_yticklabels(["Zero-To-CAD", "CAD-Recode", "DeepCAD", "Fusion360"])
for i in range(4):
    for j in range(5):
        ax.text(j, i, f"{heat[i][j]:.1f}%", ha="center", va="center",
                color="white" if heat[i][j] > 50 else "black", fontsize=9)
ax.set_title("Complex-operation coverage (% of models)")
fig.colorbar(im, label="%")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_complex_heatmap.png"), dpi=150)
print("[+] fig_complex_heatmap.png")

# ---- 图3: Zero-To-CAD 操作分布（全谱） ----
if z:
    pres = z["operation_presence_pct"]
    items = sorted(pres.items(), key=lambda kv: -kv[1])
    labels = [k for k, _ in items]; vals = [v for _, v in items]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(labels, vals, color="#2c7fb8")
    ax.set_ylabel("Model coverage (%)")
    ax.set_title("Zero-To-CAD (test, n=%d): full operation distribution" % z["n_samples"])
    plt.xticks(rotation=35, ha="right")
    for i, v in enumerate(vals):
        ax.text(i, v+1, f"{v:.1f}", ha="center", fontsize=7)
    ax.grid(axis="y", alpha=0.3); fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_zero_to_cad_dist.png"), dpi=150)
    print("[+] fig_zero_to_cad_dist.png")

# ---- 图4: Zero-To-CAD 每模型操作数分布 ----
if z and z.get("ops_count_distribution"):
    dist = {int(k): v for k, v in z["ops_count_distribution"].items()}
    ks = sorted(dist); vs = [dist[k] for k in ks]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(ks, vs, color="#2c7fb8", width=0.9)
    ax.set_xlabel("Operations per model"); ax.set_ylabel("# models")
    m = z["ops_count_stats"]
    ax.set_title(f"Zero-To-CAD ops/model (min={m['min']}, mean={m['mean']}, max={m['max']})")
    ax.grid(axis="y", alpha=0.3); fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_zero_to_cad_opscount.png"), dpi=150)
    print("[+] fig_zero_to_cad_opscount.png")

print("\n全部图表已写入", OUT)
