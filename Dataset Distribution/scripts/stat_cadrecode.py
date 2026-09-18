"""
统计 cad-recode 数据集 val 子集的操作分布（解析 CadQuery Python 代码）。

cad-recode 数据集每条是一段可执行 CadQuery 代码（约 1M train + 1k val）。
整库 354MB，val 很小。优先用 datasets 流式读取。

用法:
    set HF_ENDPOINT=https://hf-mirror.com
    python stat_cadrecode.py --split validation --limit 1000
"""
import argparse, json, re, os
from collections import Counter

OP_PATTERNS = {
    "extrude":  r"\bextrude\b",
    "revolve":  r"\brevolve\b",
    "loft":     r"\bloft\b",
    "sweep":    r"\bsweep\b",
    "chamfer":  r"\bchamfer\b",
    "fillet":   r"\bfillet\b",
    "shell":    r"\bshell\b",
    "boolean_cut":   r"\b(cut|subtract)\b",
    "boolean_union": r"\b(union|combine)\b",
    "boolean_intersect": r"\bintersect\b",
}
SKETCH_PATTERNS = {
    "line":    r"\b(line|lineTo|polyline|hLine|vLine|hLineTo|vLineTo)\b",
    "arc":     r"\b(arc|threePointArc|radiusArc|sagittaArc|tangentArcPoint)\b",
    "circle":  r"\b(circle)\b",
    "rect":    r"\b(rect|box)\b",
    "spline":  r"\b(spline|bezier|parametricCurve)\b",
    "polygon": r"\b(polygon)\b",
}

def find_code_field(ex):
    """cad-recode 列名未知，自动找最像代码的字符串字段。"""
    best = None
    for k, v in ex.items():
        if isinstance(v, str) and ("cq." in v or "Workplane" in v or "extrude" in v or "import" in v):
            if best is None or len(v) > len(best):
                best = v
    if best is None:
        # 退而求其次：最长的字符串字段
        strs = [(k, v) for k, v in ex.items() if isinstance(v, str)]
        if strs:
            best = max(strs, key=lambda kv: len(kv[1]))[1]
    return best or ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="validation")
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--repo", default="filapro/cad-recode")
    ap.add_argument("--local-dir", default=None, help="本地 .py 目录(优先)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.local_dir:
        import glob
        pyfiles = sorted(glob.glob(os.path.join(args.local_dir, "**", "*.py"), recursive=True))
        print(f"[*] 本地模式: {len(pyfiles)} 个 .py @ {args.local_dir}", flush=True)
        def gen():
            for fp in pyfiles:
                try:
                    yield {"code": open(fp, encoding="utf-8").read()}
                except Exception:
                    continue
        ds = gen()
    else:
        from datasets import load_dataset
        print(f"[*] 流式加载 {args.repo} split={args.split} ...", flush=True)
        try:
            ds = load_dataset(args.repo, split=args.split, streaming=True)
        except Exception as e:
            print("  split 名可能不同，尝试 'val' / 'test':", e)
            ds = load_dataset(args.repo, split="val", streaming=True)

    n = 0
    op_presence = Counter(); op_total = Counter()
    prim_presence = Counter()
    seq_len_list = []
    complex_ops = ["loft", "revolve", "sweep", "chamfer", "fillet"]
    models_with_complex = 0
    printed_field = False

    for ex in ds:
        if n >= args.limit: break
        n += 1
        code = find_code_field(ex)
        if not printed_field:
            print("  样例字段:", list(ex.keys()))
            print("  代码片段:", code[:200].replace("\n", " "))
            printed_field = True
        # 操作
        model_ops = set()
        n_op_lines = 0
        for name, pat in OP_PATTERNS.items():
            c = len(re.findall(pat, code, re.IGNORECASE))
            if c:
                op_presence[name] += 1; op_total[name] += c
                model_ops.add(name); n_op_lines += c
        for name, pat in SKETCH_PATTERNS.items():
            if re.search(pat, code, re.IGNORECASE):
                prim_presence[name] += 1
        if model_ops & set(complex_ops):
            models_with_complex += 1
        # 序列长度近似：代码行数
        seq_len_list.append(code.count("\n") + 1)
        if n % 200 == 0:
            print(f"    ...{n}", flush=True)

    def pct(x): return round(100*x/n, 2) if n else 0
    s = sorted(seq_len_list)
    result = {
        "dataset": args.repo, "split": args.split, "n_samples": n,
        "operation_presence_pct": {k: pct(v) for k, v in op_presence.most_common()},
        "operation_total_occurrences": dict(op_total.most_common()),
        "sketch_primitive_presence_pct": {k: pct(v) for k, v in prim_presence.most_common()},
        "complex_ops_coverage_pct": {op: pct(op_presence.get(op, 0)) for op in complex_ops},
        "models_with_any_complex_op_pct": pct(models_with_complex),
        "code_lines_stats": {"min": s[0] if s else None, "median": s[len(s)//2] if s else None,
                              "max": s[-1] if s else None,
                              "mean": round(sum(s)/len(s),2) if s else None},
    }
    outdir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(outdir, exist_ok=True)
    outpath = args.out or os.path.join(outdir, f"cadrecode_{args.split}_stats.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("="*60); print(f"cad-recode {args.split} — {n} 条"); print("="*60)
    print("[操作覆盖率%]", result["operation_presence_pct"])
    print("[复杂操作%]", result["complex_ops_coverage_pct"])
    print("[图元%]", result["sketch_primitive_presence_pct"])
    print(f"[+] 写入 {outpath}")

if __name__ == "__main__":
    main()
