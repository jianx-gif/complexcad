"""1M 全量转换驱动 (2 次执行验证流程, 流式只读代码列, 每源文件单独出 parquet 可续传)。
常驻 worker 池跨文件复用; 已存在输出的源文件跳过(断点续传)。
用法: python convert_1m.py --split train [--timeout 20] [--workers 16]
"""
import sys, os, json, argparse, time, threading, queue
from collections import Counter
import pyarrow as pa
import pyarrow.parquet as pq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import convert_fast as cf

RECYCLE = 400
REPO = "ADSKAILab/Zero-To-CAD-1m"

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
    tbl = pa.table({
        "uuid": pa.array(cols["uuid"], pa.string()),
        "cadquery_file": pa.array(cols["cadquery_file"], pa.string()),
        "cadquery_file_orig": pa.array(cols["cadquery_file_orig"], pa.string()),
        "scale": pa.array(cols["scale"], pa.float64()),
        "max_dim_mm": pa.array(cols["max_dim_mm"], pa.float64()),
        "offs": pa.array(cols["offs"], pa.string()),
        "n_scaled": pa.array(cols["n_scaled"], pa.int32()),
    })
    pq.write_table(tbl, path, compression="zstd")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="train")
    ap.add_argument("--outdir", default="Zero-To-CAD-Baseline/data/koor_1m")
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()
    cf.TIMEOUT = args.timeout

    from huggingface_hub import HfFileSystem
    fs = HfFileSystem()
    files = sorted(fs.glob(f"datasets/{REPO}/data/{args.split}/*.parquet"))
    odir = os.path.join(args.outdir, args.split)
    os.makedirs(odir, exist_ok=True)
    print(f"[{args.split}] 共 {len(files)} 个源文件, workers={args.workers} timeout={args.timeout}s", flush=True)

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(args.workers)]
    for t in threads: t.start()

    t0 = time.time(); done_files = 0; done_rows = 0; kept_rows = 0
    for fi, hf in enumerate(files):
        name = hf.split("/")[-1]
        outp = os.path.join(odir, name)
        if os.path.exists(outp):
            done_files += 1
            continue
        try:
            pf = pq.ParquetFile(fs.open(hf))
            t = pf.read(columns=["uuid", "cadquery_file"])
        except Exception as e:
            print(f"  [skip-read] {name}: {e}", flush=True)
            continue
        uu = t.column("uuid"); cc = t.column("cadquery_file")
        codes = []
        for i in range(t.num_rows):
            v = cc[i].as_py()
            if isinstance(v, (bytes, bytearray)):
                v = bytes(v).decode("utf-8", "replace")
            codes.append((uu[i].as_py(), v))
        # 派发该文件全部任务
        idmap = {}
        for j, (uuid, code) in enumerate(codes):
            idmap[j] = (uuid, code)
            task_q.put((j, code))
        # 收集该文件全部结果
        results = {}
        while len(results) < len(codes):
            tid, d = result_q.get()
            results[tid] = d
        kept = []; dropped = []
        for j, (uuid, code) in idmap.items():
            d = results[j]
            if "error" in d:
                dropped.append({"uuid": uuid, "code": code, "stage": d.get("stage"), "error": d.get("error")})
            else:
                kept.append((uuid, code, d))
        write_parquet(outp + ".tmp", kept)
        os.replace(outp + ".tmp", outp)          # 原子写, 避免半截文件
        with open(os.path.join(odir, name + ".dropped.jsonl"), "w") as fp:
            for x in dropped:
                fp.write(json.dumps(x, ensure_ascii=False) + "\n")
        done_files += 1; done_rows += len(codes); kept_rows += len(kept)
        if (fi + 1) % 1 == 0:
            dt = time.time() - t0
            rate = done_rows / max(1e-6, dt)
            eta = (len(files) - done_files) * (done_rows / max(1, fi + 1 - 0)) / max(1e-6, rate) / 3600
            print(f"  [{args.split}] 文件 {done_files}/{len(files)} 行 {done_rows} 保留 {kept_rows} "
                  f"({100*kept_rows/max(1,done_rows):.0f}%) {rate:.1f}/s ETA~{eta:.1f}h", flush=True)

    for _ in threads:
        task_q.put(SENTINEL)
    for t in threads:
        t.join(timeout=5)
    print(f"[{args.split}] 全部完成 文件={done_files} 行={done_rows} 保留={kept_rows} 用时{(time.time()-t0)/3600:.1f}h", flush=True)


if __name__ == "__main__":
    main()
