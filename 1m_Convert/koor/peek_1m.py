"""随时查看 1M 转换的中间结果: 进度 + 抽样转换后代码。
用法: python peek_1m.py [--split train] [--n 3] [--dump DIR]"""
import os, glob, argparse, random
import pyarrow.parquet as pq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="Zero-To-CAD-Baseline/data/koor_1m/train")
    ap.add_argument("--total", type=int, default=2193)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--dump", default="")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.dir, "*.parquet")))
    print(f"=== 进度: {len(files)}/{args.total} 个源文件已完成 ({100*len(files)/args.total:.1f}%) ===")
    if not files:
        print("(还没有产出文件)"); return
    # 统计已完成的行数 / scale 分布
    tot = big = 0
    for f in files:
        m = pq.read_metadata(f)
        tot += m.num_rows
    print(f"已转换并保留: ~{tot} 行 (跨 {len(files)} 文件)")

    # 抽样展示
    rng = random.Random()
    f = rng.choice(files)
    t = pq.read_table(f).to_pylist()
    rng.shuffle(t)
    if args.dump:
        os.makedirs(args.dump, exist_ok=True)
    print(f"\n=== 抽样 {min(args.n,len(t))} 个 (来自 {os.path.basename(f)}) ===")
    for r in t[:args.n]:
        print("=" * 60)
        print(f"uuid={r['uuid']}  scale={r['scale']}  max_dim={r['max_dim_mm']:.1f}mm  offs={r['offs']}")
        print("--- 转换后 cadquery_file ---")
        print(r["cadquery_file"][:500])
        if args.dump:
            u = r["uuid"][:8]
            open(f"{args.dump}/{u}_orig.py", "w").write(r["cadquery_file_orig"])
            open(f"{args.dump}/{u}_koor.py", "w").write(r["cadquery_file"])
    if args.dump:
        print(f"\n配对文件已写到 {args.dump}/")


if __name__ == "__main__":
    main()
