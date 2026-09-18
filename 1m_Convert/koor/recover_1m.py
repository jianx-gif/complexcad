"""恢复 pass: 对 1M train 里"原始能跑但缩放后失败"的模型重试。
招数: 长超时(90s, 救timeout) + min_mag=1(非零长度至少0.01mm, 救取整退化)。
只重试 stage in (scaled, verify) 的; orig 阶段(原始就崩)跳过。
恢复成功的写到 koor_1m/train/ 下 <原文件名>.rec.parquet (glob *.parquet 自动并入)。
可续传: 已有 .rec.parquet 的源文件跳过。
"""
import sys, os, glob, json, argparse, time, threading, queue
import pyarrow as pa
import pyarrow.parquet as pq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import convert_fast as cf

RECYCLE = 400
task_q = queue.Queue(maxsize=4000)
result_q = queue.Queue()
SENTINEL = None


def worker():
    p = cf.spawn(); n = 0
    while True:
        item = task_q.get()
        if item is SENTINEL:
            break
        tid, code = item
        d = cf.process(p, code)
        if d.get("stage") in ("orig", "scaled") and d.get("error") in ("timeout", "crash"):
            try: p.kill()
            except Exception: pass
            p = cf.spawn(); n = 0
        result_q.put((tid, d))
        n += 1
        if n >= RECYCLE:
            try: p.kill()
            except Exception: pass
            p = cf.spawn(); n = 0
    try: p.kill()
    except Exception: pass


def write_parquet(path, rows):
    cols = {k: [] for k in ("uuid", "cadquery_file", "cadquery_file_orig",
                            "scale", "max_dim_mm", "offs", "n_scaled")}
    for uuid, code, d in rows:
        cols["uuid"].append(uuid); cols["cadquery_file"].append(d["scaled"])
        cols["cadquery_file_orig"].append(code); cols["scale"].append(float(d["scale"]))
        cols["max_dim_mm"].append(float(d["max_dim"])); cols["offs"].append(json.dumps(d["offs"]))
        cols["n_scaled"].append(int(d["n_scaled"]))
    pq.write_table(pa.table({
        "uuid": pa.array(cols["uuid"], pa.string()),
        "cadquery_file": pa.array(cols["cadquery_file"], pa.string()),
        "cadquery_file_orig": pa.array(cols["cadquery_file_orig"], pa.string()),
        "scale": pa.array(cols["scale"], pa.float64()),
        "max_dim_mm": pa.array(cols["max_dim_mm"], pa.float64()),
        "offs": pa.array(cols["offs"], pa.string()),
        "n_scaled": pa.array(cols["n_scaled"], pa.int32()),
    }), path, compression="zstd")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="Zero-To-CAD-Baseline/data/koor_1m/train")
    ap.add_argument("--timeout", type=int, default=90)
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()
    cf.TIMEOUT = args.timeout
    cf.MIN_MAG = 1                       # 防退化: 非零长度至少 1 单位(0.01mm)

    dfiles = sorted(glob.glob(os.path.join(args.dir, "*.dropped.jsonl")))
    print(f"共 {len(dfiles)} 个 dropped 文件, timeout={args.timeout}s, min_mag=1", flush=True)
    threads = [threading.Thread(target=worker, daemon=True) for _ in range(args.workers)]
    for t in threads: t.start()

    t0 = time.time(); tot_try = tot_rec = done_files = 0
    for fi, df in enumerate(dfiles):
        base = df[:-len(".dropped.jsonl")]
        recp = base + ".rec.parquet"
        if os.path.exists(recp):
            done_files += 1; continue
        # 读该文件被丢的, 只重试非 orig 阶段
        retry = []
        for line in open(df):
            try: x = json.loads(line)
            except Exception: continue
            if x.get("stage") in ("scaled", "verify"):
                retry.append((x["uuid"], x["code"]))
        if not retry:
            open(recp, "ab").close()      # 占位空文件? 不, 写空parquet
            write_parquet(recp, [])
            done_files += 1; continue
        idmap = {}
        for j, (uuid, code) in enumerate(retry):
            idmap[j] = (uuid, code); task_q.put((j, code))
        results = {}
        while len(results) < len(retry):
            tid, d = result_q.get(); results[tid] = d
        rec = []
        for j, (uuid, code) in idmap.items():
            d = results[j]
            if "error" not in d:
                rec.append((uuid, code, d))
        write_parquet(recp, rec)
        tot_try += len(retry); tot_rec += len(rec); done_files += 1
        if (fi + 1) % 20 == 0:
            dt = time.time() - t0
            print(f"  文件 {done_files}/{len(dfiles)} 重试 {tot_try} 救回 {tot_rec} "
                  f"({100*tot_rec/max(1,tot_try):.0f}%) {tot_try/max(1e-6,dt):.1f}/s "
                  f"ETA~{(len(dfiles)-done_files)/max(1e-6,(done_files)/dt)/3600:.1f}h", flush=True)

    for _ in threads: task_q.put(SENTINEL)
    for t in threads: t.join(timeout=5)
    print(f"恢复完成: 重试 {tot_try} 救回 {tot_rec} ({100*tot_rec/max(1,tot_try):.1f}%) 用时{(time.time()-t0)/3600:.1f}h", flush=True)


if __name__ == "__main__":
    main()
