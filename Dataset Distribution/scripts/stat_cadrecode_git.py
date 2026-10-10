r"""
快速统计 cad-recode-v1.5 训练集（~98 万个 .py）的操作分布。

不逐个打开小文件（Windows 上 ~100 文件/秒，太慢），而是直接从本地 git 仓库的 packfile
用 `git cat-file --batch` 顺序流式读取 blob，快一个数量级以上。
统计口径与 stat_cadrecode.py 完全一致（复用其 OP_PATTERNS / SKETCH_PATTERNS）。

用法:
    python stat_cadrecode_git.py --repo-dir "<datasets>\cadrecode_v15_train" --subdir train --split v15_train
    python stat_cadrecode_git.py --repo-dir "<datasets>\cadrecode_v15_train" --subdir val   --split v15_validation
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))  # repository root
import argparse, json, os, re, subprocess, sys, time
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from stat_cadrecode import OP_PATTERNS, SKETCH_PATTERNS  # 保持口径一致

OP_RE = {k: re.compile(v, re.IGNORECASE) for k, v in OP_PATTERNS.items()}
SK_RE = {k: re.compile(v, re.IGNORECASE) for k, v in SKETCH_PATTERNS.items()}
COMPLEX = ["loft", "revolve", "sweep", "chamfer", "fillet"]
# CAD-Recode 里直线草图叫 .segment()，补进 line 口径；命令数口径与 DeepCAD 对齐（草图图元 + 建模操作）
SK_RE["line"] = re.compile(r"\b(line|lineTo|polyline|hLine|vLine|hLineTo|vLineTo|segment)\b", re.IGNORECASE)
CMD_RE = re.compile(r"\.(segment|arc|circle|rect|extrude|cylinder|box|union)\(")


def iter_blobs(repo_dir, subdir):
    """yield (path, code_str) for every *.py under subdir, streamed from the git object store."""
    ls = subprocess.run(
        ["git", "-C", repo_dir, "ls-tree", "-r", "-z", "HEAD", "--", subdir],
        capture_output=True, check=True)
    entries = []
    for rec in ls.stdout.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        if not path.endswith(b".py"):
            continue
        sha = meta.split(b" ")[2]
        entries.append((sha, path.decode("utf-8", "replace")))
    print(f"[*] git ls-tree: {len(entries)} 个 .py", flush=True)

    p = subprocess.Popen(["git", "-C", repo_dir, "cat-file", "--batch"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1 << 20)

    # 写入端用线程喂 sha，避免管道死锁
    import threading
    def feeder():
        for sha, _ in entries:
            p.stdin.write(sha + b"\n")
        p.stdin.close()
    threading.Thread(target=feeder, daemon=True).start()

    out = p.stdout
    for sha, path in entries:
        header = out.readline()  # b"<sha> blob <size>\n"
        parts = header.split()
        if len(parts) < 3 or parts[1] != b"blob":
            continue
        size = int(parts[2])
        data = out.read(size)
        out.read(1)  # trailing newline
        yield path, data.decode("utf-8", "replace")
    p.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-dir", required=True)
    ap.add_argument("--subdir", default="train")
    ap.add_argument("--split", default="v15_train")
    ap.add_argument("--dataset-name", default="filapro/cad-recode-v1.5")
    ap.add_argument("--limit", type=int, default=0, help="0=全部")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    n = 0
    op_presence = Counter(); op_total = Counter(); prim_presence = Counter()
    seq_len_list = []; models_with_complex = 0
    n_ops_per_model = Counter()
    cmd_len_list = []; cmd_hist = Counter()
    t0 = time.time()

    for path, code in iter_blobs(args.repo_dir, args.subdir):
        if args.limit and n >= args.limit:
            break
        n += 1
        model_ops = set(); n_op_calls = 0
        for name, rx in OP_RE.items():
            c = len(rx.findall(code))
            if c:
                op_presence[name] += 1; op_total[name] += c
                model_ops.add(name); n_op_calls += c
        for name, rx in SK_RE.items():
            if rx.search(code):
                prim_presence[name] += 1
        if model_ops & set(COMPLEX):
            models_with_complex += 1
        seq_len_list.append(code.count("\n") + 1)
        k = len(CMD_RE.findall(code)); cmd_len_list.append(k); cmd_hist[k] += 1
        n_ops_per_model[n_op_calls] += 1
        if n % 50000 == 0:
            print(f"    ...{n}  ({n/(time.time()-t0):.0f}/s)", flush=True)

    def pct(x): return round(100 * x / n, 2) if n else 0
    s = sorted(seq_len_list); cs = sorted(cmd_len_list)
    result = {
        "dataset": args.dataset_name, "split": args.split, "n_samples": n,
        "operation_presence_pct": {k: pct(v) for k, v in op_presence.most_common()},
        "operation_total_occurrences": dict(op_total.most_common()),
        "sketch_primitive_presence_pct": {k: pct(v) for k, v in prim_presence.most_common()},
        "complex_ops_coverage_pct": {op: pct(op_presence.get(op, 0)) for op in COMPLEX},
        "models_with_any_complex_op_pct": pct(models_with_complex),
        "code_lines_stats": {"min": s[0] if s else None, "median": s[len(s) // 2] if s else None,
                             "max": s[-1] if s else None,
                             "mean": round(sum(s) / len(s), 2) if s else None},
        "op_calls_per_model_hist": dict(sorted(n_ops_per_model.items())),
        "sequence_length_stats": {"min": cs[0] if cs else None, "median": cs[len(cs) // 2] if cs else None,
                                  "mean": round(sum(cs) / len(cs), 2) if cs else None,
                                  "p90": cs[int(len(cs) * 0.9)] if cs else None, "max": cs[-1] if cs else None,
                                  "definition": "count of sketch primitives (segment/arc/circle/rect) + modeling ops "
                                                "(extrude/cylinder/box/union) per model, aligned with DeepCAD command-count"},
        "sequence_length_distribution": {str(k): v for k, v in sorted(cmd_hist.items())},
        "sketch_primitive_presence_pct_note": "line = CadQuery sketch .segment(); spline/polygon = 0 (not in vocabulary)",
        "method": "git cat-file --batch streaming; regex same as stat_cadrecode.py",
    }
    outdir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(outdir, exist_ok=True)
    outpath = args.out or os.path.join(outdir, f"cadrecode_{args.split}_stats.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("=" * 60); print(f"cad-recode {args.split} — {n} 条  ({time.time()-t0:.0f}s)"); print("=" * 60)
    print("[操作覆盖率%]", result["operation_presence_pct"])
    print("[复杂操作%]", result["complex_ops_coverage_pct"])
    print("[图元%]", result["sketch_primitive_presence_pct"])
    print("[代码行数]", result["code_lines_stats"])
    print("[命令数/模型]", result["sequence_length_stats"])
    print(f"[+] 写入 {outpath}")


if __name__ == "__main__":
    main()
