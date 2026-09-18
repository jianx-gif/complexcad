"""
统计 Zero-To-CAD-1m 数据集的 test 子集分布（操作类型/操作数/草图图元/复杂度）。

策略：流式读取 HF parquet，只取需要的文本列（cadquery_ops_json / cadquery_ops_count /
num_faces / cadquery_file），不下载 image/stl/step 字节，避免几百 GB 落盘。

用法:
    set HF_ENDPOINT=https://hf-mirror.com   (国内加速，可选)
    python stat_zero_to_cad.py --split test --limit 10000

输出: out/zero_to_cad_<split>_stats.json  +  控制台摘要
"""
import argparse, json, re, os, sys
from collections import Counter

# 我们关心的建模操作（CadQuery 方法名 -> 归一化操作类别）
# 复杂操作是论文重点
OP_PATTERNS = {
    "extrude":  r"\bextrude\b",
    "revolve":  r"\brevolve\b",
    "loft":     r"\bloft\b",
    "sweep":    r"\bsweep\b",
    "chamfer":  r"\bchamfer\b",
    "fillet":   r"\bfillet\b",
    "shell":    r"\bshell\b",
    "boolean_union": r"\b(union|combine)\b",
    "boolean_cut":   r"\b(cut|subtract)\b",
    "boolean_intersect": r"\bintersect\b",
    "pattern":  r"\b(polarArray|rarray|mirror|eachpoint)\b",
}
# 草图图元
SKETCH_PATTERNS = {
    "line":    r"\b(line|lineTo|polyline|hLine|vLine|hLineTo|vLineTo)\b",
    "arc":     r"\b(arc|threePointArc|radiusArc|sagittaArc|tangentArcPoint)\b",
    "circle":  r"\b(circle)\b",
    "rect":    r"\b(rect|box)\b",
    "spline":  r"\b(spline|bezier|parametricCurve)\b",
    "polygon": r"\b(polygon)\b",
}

def _to_text(v):
    """字段可能是 str / bytes / None，统一转成 str。"""
    if v is None:
        return ""
    if isinstance(v, bytes):
        try:
            return v.decode("utf-8", errors="ignore")
        except Exception:
            return ""
    return str(v)

def analyze_ops_json(ops_json_str):
    """优先用数据集自带的 cadquery_ops_json 字段（最准）。返回操作名列表 或 None。"""
    ops_json_str = _to_text(ops_json_str)
    if not ops_json_str:
        return None
    try:
        ops = json.loads(ops_json_str)
        # ops 可能是 list[str] 或 list[dict]
        names = []
        for o in ops:
            if isinstance(o, str):
                names.append(o.lower())
            elif isinstance(o, dict):
                # 取常见键
                for k in ("op", "name", "type", "operation"):
                    if k in o:
                        names.append(str(o[k]).lower())
                        break
        return names
    except Exception:
        return None

def analyze_code(code):
    """从 CadQuery 源码文本正则匹配操作与图元（兜底/补充）。"""
    ops = Counter()
    prims = Counter()
    code = _to_text(code)
    if not code:
        return ops, prims
    low = code
    for name, pat in OP_PATTERNS.items():
        n = len(re.findall(pat, low, flags=re.IGNORECASE))
        if n:
            ops[name] += n
    for name, pat in SKETCH_PATTERNS.items():
        n = len(re.findall(pat, low, flags=re.IGNORECASE))
        if n:
            prims[name] += n
    return ops, prims

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="test", choices=["test", "validation", "train"])
    ap.add_argument("--limit", type=int, default=100000, help="最多统计多少条")
    ap.add_argument("--repo", default="ADSKAILab/Zero-To-CAD-1m")
    ap.add_argument("--local-dir", default=None, help="本地 parquet 目录(优先，离线无限流)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    # 只读统计需要的列，避免解码 image/stl/step 字节
    WANT_COLS = ["cadquery_ops_json", "cadquery_ops_count", "num_faces", "cadquery_file"]

    if args.local_dir:
        import glob, pyarrow.parquet as pq
        files = sorted(glob.glob(os.path.join(args.local_dir, "**", "*.parquet"), recursive=True))
        print(f"[*] 本地模式: {len(files)} 个 parquet @ {args.local_dir}", flush=True)

        def iter_rows():
            for fp in files:
                pf = pq.ParquetFile(fp)
                cols = [c for c in WANT_COLS if c in pf.schema_arrow.names]
                for batch in pf.iter_batches(batch_size=512, columns=cols):
                    d = batch.to_pydict()
                    m = len(next(iter(d.values())))
                    for i in range(m):
                        yield {k: d[k][i] for k in d}
        ds = iter_rows()
    else:
        from datasets import load_dataset
        print(f"[*] 流式加载 {args.repo} split={args.split} (limit={args.limit}) ...", flush=True)
        ds = load_dataset(args.repo, split=args.split, streaming=True)

    # 统计容器
    n = 0
    op_presence = Counter()        # 含某操作的"模型数"（每模型计一次）
    op_total = Counter()           # 某操作的"总出现次数"
    prim_presence = Counter()
    ops_count_hist = Counter()     # cadquery_ops_count 分布
    num_faces_list = []
    complex_ops = ["loft", "revolve", "sweep", "chamfer", "fillet"]
    models_with_any_complex = 0
    used_ops_json = 0
    used_code = 0

    for ex in ds:
        if n >= args.limit:
            break
        n += 1

        if n == 1:
            # 诊断：打印字段名与关键字段的类型/样例
            print("  [字段]", list(ex.keys()), flush=True)
            for fld in ("cadquery_ops_json", "cadquery_ops_count", "num_faces"):
                v = ex.get(fld)
                print(f"  [{fld}] type={type(v).__name__} sample={_to_text(v)[:160]}", flush=True)

        # 1) 操作：优先 ops_json（含 function 串，如 cq.Workplane.moveTo.lineTo...）
        names = analyze_ops_json(ex.get("cadquery_ops_json"))
        per_model_ops = Counter()
        if names is not None and len(names) > 0:
            used_ops_json += 1
            for nm in names:
                matched = None
                for cat, pat in OP_PATTERNS.items():
                    if re.search(pat, nm, flags=re.IGNORECASE):
                        matched = cat
                        break
                if matched:
                    per_model_ops[matched] += 1
        else:
            ops, _ = analyze_code(_to_text(ex.get("cadquery_file", "")))
            if ops:
                used_code += 1
            per_model_ops = ops

        # 图元 presence：合并 ops_json 的 function 串 + 源码，做一次去重统计（每模型每图元计1次）
        prim_text = " ".join(names) if names else ""
        prim_text += " " + _to_text(ex.get("cadquery_file", ""))
        _, prims_in_model = analyze_code(prim_text)
        for p in prims_in_model:          # prims_in_model 已是 Counter，对 key 去重计一次
            prim_presence[p] += 1

        # 汇总操作
        for op, c in per_model_ops.items():
            op_presence[op] += 1
            op_total[op] += c

        # 复杂操作覆盖
        if any(op_presence and any(re.search(c, k) for c in complex_ops) for k in per_model_ops):
            pass
        if any(k in complex_ops for k in per_model_ops):
            models_with_any_complex += 1

        # ops_count / faces
        oc = ex.get("cadquery_ops_count")
        if oc is not None:
            ops_count_hist[int(oc)] += 1
        nf = ex.get("num_faces")
        if nf is not None:
            try:
                num_faces_list.append(int(nf))
            except Exception:
                pass

        if n % 1000 == 0:
            print(f"    ...已处理 {n} 条", flush=True)

    # 汇总输出
    def pct(x):
        return round(100.0 * x / n, 2) if n else 0.0

    faces_sorted = sorted(num_faces_list)
    def q(p):
        if not faces_sorted: return None
        i = min(len(faces_sorted)-1, int(p*len(faces_sorted)))
        return faces_sorted[i]

    result = {
        "dataset": args.repo,
        "split": args.split,
        "n_samples": n,
        "source_field_used": {"cadquery_ops_json": used_ops_json, "code_regex_fallback": used_code},
        "operation_presence_count": dict(op_presence.most_common()),
        "operation_presence_pct": {k: pct(v) for k, v in op_presence.most_common()},
        "operation_total_occurrences": dict(op_total.most_common()),
        "sketch_primitive_presence_count": dict(prim_presence.most_common()),
        "sketch_primitive_presence_pct": {k: pct(v) for k, v in prim_presence.most_common()},
        "complex_ops_coverage": {
            "complex_ops_tracked": complex_ops,
            "models_with_any_complex_op": models_with_any_complex,
            "models_with_any_complex_op_pct": pct(models_with_any_complex),
            "per_op_presence_pct": {op: pct(op_presence.get(op, 0)) for op in complex_ops},
        },
        "ops_count_distribution": dict(sorted(ops_count_hist.items())),
        "ops_count_stats": {
            "min": min(ops_count_hist) if ops_count_hist else None,
            "max": max(ops_count_hist) if ops_count_hist else None,
            "mean": round(sum(k*v for k,v in ops_count_hist.items())/n, 2) if n and ops_count_hist else None,
        },
        "num_faces_stats": {
            "min": faces_sorted[0] if faces_sorted else None,
            "median": q(0.5),
            "p90": q(0.9),
            "max": faces_sorted[-1] if faces_sorted else None,
            "mean": round(sum(faces_sorted)/len(faces_sorted), 2) if faces_sorted else None,
        },
    }

    outdir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(outdir, exist_ok=True)
    outpath = args.out or os.path.join(outdir, f"zero_to_cad_{args.split}_stats.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 控制台摘要
    print("\n" + "="*60)
    print(f"Zero-To-CAD  {args.split}  —  统计 {n} 条")
    print("="*60)
    print("\n[操作覆盖率 %（含该操作的模型占比）]")
    for k, v in result["operation_presence_pct"].items():
        print(f"   {k:20s} {v:6.2f}%   (出现总次数 {op_total.get(k,0)})")
    print("\n[复杂操作覆盖]")
    for op in complex_ops:
        print(f"   {op:10s} {result['complex_ops_coverage']['per_op_presence_pct'][op]:6.2f}%")
    print(f"   >> 含任一复杂操作的模型: {result['complex_ops_coverage']['models_with_any_complex_op_pct']}%")
    print("\n[草图图元覆盖率 %]")
    for k, v in result["sketch_primitive_presence_pct"].items():
        print(f"   {k:10s} {v:6.2f}%")
    print("\n[每模型操作数] ", result["ops_count_stats"])
    print("[面数 num_faces] ", result["num_faces_stats"])
    print(f"\n[+] 结果已写入 {outpath}")

if __name__ == "__main__":
    main()
