"""
统计 DeepCAD 数据集 test 子集的操作分布。

DeepCAD 官方数据有两种形式：
  (A) cad_vec/*.h5 ：向量化序列，每行 [cmd_type, params...]，cmd_type:
        0=Line 1=Arc 2=Circle 3=EOS 4=SOL 5=Extrude（官方 macro.py 定义）
  (B) cad_json/*.json ：原始 Onshape 解析序列
官方仓库 github.com/ChrisWu1997/DeepCAD ；数据走 Google Drive。
HF 镜像: 可搜 'deepcad' 数据集；若用 .h5，传 --h5dir。

本脚本支持 .h5（优先）或 .json 目录。DeepCAD 词表本就只有 sketch(line/arc/circle)+extrude，
统计结果应直接显示 revolve/loft/sweep/chamfer/fillet = 0%，作为 Challenge 1 的硬证据。

用法:
    python stat_deepcad.py --h5dir "E:\path\to\cad_vec"  [--limit 8946]
    或
    python stat_deepcad.py --jsondir "E:\path\to\cad_json"
"""
import argparse, json, os, glob
from collections import Counter

# DeepCAD macro.py 命令定义
CMD_NAMES = {0: "line", 1: "arc", 2: "circle", 3: "EOS", 4: "SOL", 5: "extrude"}

def stat_h5(h5dir, limit, file_list=None):
    import h5py, numpy as np
    if file_list is not None:
        files = file_list
    else:
        files = sorted(glob.glob(os.path.join(h5dir, "**", "*.h5"), recursive=True))
    if limit: files = files[:limit]
    print(f"[*] {len(files)} 个 .h5")
    n = 0
    cmd_total = Counter(); prim_presence = Counter()
    seq_len_list = []; ext_per_model = []
    for fp in files:
        try:
            with h5py.File(fp, "r") as f:
                key = "vec" if "vec" in f else list(f.keys())[0]
                vec = f[key][:]
        except Exception:
            continue
        n += 1
        cmds = vec[:, 0].astype(int)
        real = [c for c in cmds if c != 3]  # 去 EOS padding
        seq_len_list.append(len(real))
        present = set()
        n_ext = 0
        for c in real:
            name = CMD_NAMES.get(int(c), f"cmd{c}")
            cmd_total[name] += 1
            if name in ("line", "arc", "circle"): present.add(name)
            if name == "extrude": n_ext += 1
        for p in present: prim_presence[p] += 1
        ext_per_model.append(n_ext)
    return n, cmd_total, prim_presence, seq_len_list, ext_per_model

def stat_json(jsondir, limit):
    files = sorted(glob.glob(os.path.join(jsondir, "**", "*.json"), recursive=True))
    if limit: files = files[:limit]
    print(f"[*] {len(files)} 个 .json")
    n = 0; cmd_total = Counter(); prim_presence = Counter()
    seq_len_list = []; ext_per_model = []
    for fp in files:
        try:
            data = json.load(open(fp, encoding="utf-8"))
        except Exception:
            continue
        n += 1
        # DeepCAD json: entities + sequence；这里粗统计 extrude/ sketch
        seq = data.get("sequence", [])
        seq_len_list.append(len(seq))
        present = set(); n_ext = 0
        for s in seq:
            t = str(s.get("type", "")).lower()
            cmd_total[t] += 1
            if "extrude" in t: n_ext += 1
        ext_per_model.append(n_ext)
    return n, cmd_total, prim_presence, seq_len_list, ext_per_model

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5dir")
    ap.add_argument("--jsondir")
    ap.add_argument("--split-json", help="train_val_test_split.json，用于只统计某个 split")
    ap.add_argument("--split", default="test", choices=["train", "validation", "test"])
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    file_list = None
    if args.split_json and args.h5dir:
        sp = json.load(open(args.split_json, encoding="utf-8"))
        ids = sp.get(args.split, [])
        # split 里是 "0067/00675619" 形式，拼成 h5 绝对路径
        file_list = [os.path.join(args.h5dir, rel + ".h5") for rel in ids]
        file_list = [p for p in file_list if os.path.exists(p)]
        print(f"[*] split={args.split}: {len(ids)} 条，命中 {len(file_list)} 个 h5")

    if args.h5dir:
        n, cmd_total, prim_presence, seq_len_list, ext_per_model = stat_h5(args.h5dir, args.limit, file_list)
    elif args.jsondir:
        n, cmd_total, prim_presence, seq_len_list, ext_per_model = stat_json(args.jsondir, args.limit)
    else:
        print("需要 --h5dir 或 --jsondir"); return

    def pct(x): return round(100*x/n, 2) if n else 0
    s = sorted(seq_len_list)
    complex_ops = ["revolve", "loft", "sweep", "chamfer", "fillet"]
    result = {
        "dataset": "DeepCAD", "n_samples": n,
        "command_total_occurrences": dict(cmd_total.most_common()),
        "sketch_primitive_presence_pct": {k: pct(v) for k, v in prim_presence.most_common()},
        "complex_ops_coverage_pct": {op: pct(cmd_total.get(op, 0)) for op in complex_ops},
        "note": "DeepCAD 词表只含 line/arc/circle/SOL/EOS/extrude；复杂操作恒为 0，是 Challenge 1 的结构性证据",
        "sequence_length_stats": {"min": s[0] if s else None, "median": s[len(s)//2] if s else None,
                                  "max": s[-1] if s else None,
                                  "mean": round(sum(s)/len(s),2) if s else None},
        "quantization": "所有连续参数量化到 256 级/8-bit（Challenge 2 证据，来自论文，非本统计）",
    }
    outdir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(outdir, exist_ok=True)
    outpath = args.out or os.path.join(outdir, "deepcad_test_stats.json")
    json.dump(result, open(outpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("="*60); print(f"DeepCAD — {n} 条"); print("="*60)
    print("[命令总计]", dict(cmd_total.most_common()))
    print("[图元%]", result["sketch_primitive_presence_pct"])
    print("[复杂操作%]", result["complex_ops_coverage_pct"])
    print("[序列长度]", result["sequence_length_stats"])
    print(f"[+] 写入 {outpath}")

if __name__ == "__main__":
    main()
