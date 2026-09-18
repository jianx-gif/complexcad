"""任务4 补充实验: 参数量化损失定量分析 (Parameter Quantization-Loss Experiment).

论证: 本数据集保留连续浮点参数, 而 DeepCAD 把所有连续参数量化到 256 级(8-bit)。
本实验把本数据集的精确参数**模拟量化到 DeepCAD 的 256 级**, 量出由此引入的精度损失
(绝对 mm + 相对 %), 给出"若采用 DeepCAD 量化方案会损失多少精度"的直接数值证据。

DeepCAD 量化方式(Wu et al. ICCV'21): 连续参数先归一化到模型尺度范围, 再线性映射到
[0, 2^b - 1] 整数(b=8 -> 256 级), 推理时反量化。量化步长 = 范围/(2^b-1)。
最大量化误差 = 半个步长。本实验对每个件的命名尺寸参数, 以该件包围盒最大边为归一化
尺度(DeepCAD 用模型整体尺度), 量化-反量化, 统计误差。

输出: precision_report/quantization_loss.json + figures/fig5_quant_loss.png
用法: python -X utf8 quantization_loss.py [--levels 256] [--limit N]
"""
import os, sys, glob, re, json, argparse, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
ROOT = os.path.dirname(PARENT)
OUTDIR = os.path.join(ROOT, "output")
REPORT = os.path.join(PARENT, "precision_report")
FIGS = os.path.join(REPORT, "figures")

PARAM_RE = re.compile(r"^([a-zA-Z_]\w*)\s*=\s*(-?\d+\.?\d*)\s*$", re.M)
# 只统计有物理长度意义的尺寸参数(排除计数/行列数等无量纲整数)
SKIP_HINT = ("count", "rows", "cols", "num", "_n", "segments", "sides", "teeth")


def parse_params(src):
    out = {}
    for nm, v in PARAM_RE.findall(src):
        low = nm.lower()
        if any(h in low for h in SKIP_HINT):
            continue
        try:
            val = float(v)
        except ValueError:
            continue
        # 跳过明显的无量纲整数计数(整数且<=20且名字不含尺寸词)
        out[nm] = val
    return out


def quantize_loss(values, levels):
    """DeepCAD 式: 用一组参数的范围做归一化, 量化到 levels 级, 反量化, 返回每参数误差(绝对)。
    DeepCAD 对整个模型的参数共用尺度; 这里用该件所有尺寸参数的 [min,max] 作归一化范围。"""
    vmin, vmax = min(values), max(values)
    rng = vmax - vmin
    if rng <= 1e-9:
        return [0.0] * len(values), 0.0
    step = rng / (levels - 1)            # 量化步长
    errs = []
    for v in values:
        q = round((v - vmin) / step)     # 量化到整数级
        v_deq = vmin + q * step          # 反量化
        errs.append(abs(v - v_deq))
    return errs, step


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--levels", type=int, default=256, help="量化级数(DeepCAD=256/8bit)")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    os.makedirs(FIGS, exist_ok=True)

    dirs = sorted(glob.glob(os.path.join(OUTDIR, "*/")))
    if args.limit:
        dirs = dirs[:args.limit]

    all_abs = []        # 所有参数的绝对误差(mm)
    all_rel = []        # 所有参数的相对误差(%)
    per_model_max = []  # 每模型最大绝对误差
    n_params = 0
    n_models = 0
    steps = []
    for d in dirs:
        f = os.path.join(d, "cadquery.py")
        if not os.path.isfile(f):
            continue
        try:
            params = parse_params(open(f, encoding="utf-8").read())
        except Exception:
            continue
        vals = [v for v in params.values()]
        if len(vals) < 2:
            continue
        errs, step = quantize_loss(vals, args.levels)
        if step == 0:
            continue
        n_models += 1
        steps.append(step)
        mx = 0.0
        for v, e in zip(vals, errs):
            all_abs.append(e)
            if abs(v) > 1e-6:
                all_rel.append(100 * e / abs(v))
            n_params += 1
            mx = max(mx, e)
        per_model_max.append(mx)

    def stats(xs):
        xs = sorted(xs)
        return {"mean": round(statistics.mean(xs), 4),
                "median": round(statistics.median(xs), 4),
                "p90": round(xs[int(len(xs) * 0.9)], 4),
                "p99": round(xs[int(len(xs) * 0.99)], 4),
                "max": round(max(xs), 4)}

    result = {
        "levels": args.levels,
        "n_models": n_models,
        "n_params": n_params,
        "abs_err_mm": stats(all_abs),
        "rel_err_pct": stats(all_rel),
        "per_model_max_abs_mm": stats(per_model_max),
        "mean_quant_step_mm": round(statistics.mean(steps), 4),
        "note": "本数据集实际损失为 0(连续浮点); 上表为'若按 DeepCAD 量化到 %d 级'的模拟损失" % args.levels,
    }
    json.dump(result, open(os.path.join(REPORT, "quantization_loss.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # 图
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.rcParams["font.size"] = 11
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
        clipped = [e for e in all_abs if e <= result["abs_err_mm"]["p99"] * 1.2]
        ax1.hist(clipped, bins=50, color="#C44E52", edgecolor="white")
        ax1.axvline(result["abs_err_mm"]["mean"], color="#333", ls="--",
                    label="mean=%.3f mm" % result["abs_err_mm"]["mean"])
        ax1.set_xlabel("Absolute parameter error (mm)")
        ax1.set_ylabel("Parameter count")
        ax1.set_title("Quantization Loss @ %d levels (DeepCAD-style)\nOurs keeps float -> loss = 0" % args.levels)
        ax1.legend()
        relc = [e for e in all_rel if e <= result["rel_err_pct"]["p99"] * 1.2]
        ax2.hist(relc, bins=50, color="#DD8452", edgecolor="white")
        ax2.axvline(result["rel_err_pct"]["mean"], color="#333", ls="--",
                    label="mean=%.2f%%" % result["rel_err_pct"]["mean"])
        ax2.set_xlabel("Relative parameter error (%)")
        ax2.set_ylabel("Parameter count")
        ax2.set_title("Relative Quantization Loss @ %d levels" % args.levels)
        ax2.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(FIGS, "fig5_quant_loss.png"), dpi=120)
        plt.close()
        figok = True
    except Exception as e:
        print("[图跳过]", type(e).__name__, str(e)[:80])
        figok = False

    print("=== 参数量化损失实验 (DeepCAD %d 级) ===" % args.levels)
    print("  统计 %d 个模型, %d 个尺寸参数" % (n_models, n_params))
    print("  绝对误差(mm): mean=%.4f median=%.4f p90=%.4f p99=%.4f max=%.4f"
          % tuple(result["abs_err_mm"][k] for k in ["mean", "median", "p90", "p99", "max"]))
    print("  相对误差(%%): mean=%.3f median=%.3f p90=%.3f max=%.3f"
          % tuple(result["rel_err_pct"][k] for k in ["mean", "median", "p90", "max"]))
    print("  每模型最大绝对误差(mm): mean=%.4f max=%.4f"
          % (result["per_model_max_abs_mm"]["mean"], result["per_model_max_abs_mm"]["max"]))
    print("  -> 本数据集保留连续浮点, 实际损失 = 0 mm")
    print("  -> 输出: quantization_loss.json" + (" + fig5_quant_loss.png" if figok else ""))


if __name__ == "__main__":
    main()
