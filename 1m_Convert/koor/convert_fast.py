"""快速全量转换 (双 bbox 调用各自独立超时, 缩放在驱动内纯 AST):
每个模型: bbox(原始)->定scale->缩放源码->bbox(缩放后)->查忠实+落盒->追加平移。
worker 只做 bbox 服务(常驻 import 一次)。卡死的单次执行 15s 强杀重启。
输出: uuid, cadquery_file(缩放+平移), cadquery_file_orig, scale, max_dim_mm, offs, n_scaled。
用法: python convert_fast.py --splits train test [--limit N] [--workers 16]
"""
import sys, os, glob, json, argparse, subprocess, threading, queue, time
from collections import Counter
import pyarrow as pa
import pyarrow.parquet as pq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from koor_transform import scale_code

TIMEOUT = 30          # 由 --timeout 覆盖
MIN_MAG = 0           # >0: 恢复模式下非零长度取整后至少保留这么多单位(防退化)
RECYCLE = 400
FIXED_SCALE, FIT_HI = 100.0, 9990.0
BOX_LO, BOX_HI = 1, 10000


# select.select() only works on sockets on Windows, not pipes; this toolchain
# was written for Linux. A per-process reader thread drains stdout into a queue
# so bbox() can wait with a timeout cross-platform without touching the logic.
def _spawn_reader(p):
    q = queue.Queue()

    def _pump():
        try:
            for line in p.stdout:
                q.put(line)
        except Exception:
            pass
        q.put(None)                      # EOF sentinel
    th = threading.Thread(target=_pump, daemon=True)
    th.start()
    p._outq = q


def spawn():
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    p = subprocess.Popen([sys.executable, os.path.join(HERE, "bbox_persistent.py")],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                         bufsize=1, encoding="utf-8", env=env)
    _spawn_reader(p)
    try:
        p._outq.get(timeout=60)          # consume READY
    except queue.Empty:
        pass
    return p


def bbox(p, code):
    """返回 (bb_or_None, ok)。bb=[xl,yl,zl,xmin,ymin,zmin]。超时/崩溃 -> (None,'timeout'/'fail')"""
    try:
        p.stdin.write(json.dumps({"code": code}) + "\n"); p.stdin.flush()
    except Exception:
        return None, "crash"
    try:
        line = p._outq.get(timeout=TIMEOUT)
    except queue.Empty:
        return None, "timeout"
    if line is None:                     # child died / EOF
        return None, "crash"
    try:
        d = json.loads(line)
    except Exception:
        return None, "crash"
    if "error" in d:
        return None, d["error"][:50]
    return d["bb"], "ok"


def process(p, src):
    """对一个模型做完整转换。返回 dict(成功) 或 {'error':...}。p 可能被替换 -> 返回新 p。"""
    ob, st = bbox(p, src)              # 1) 原始包围盒
    if ob is None:
        return {"error": st, "stage": "orig"}
    oxl, oyl, ozl = ob[0], ob[1], ob[2]
    omax = max(oxl, oyl, ozl)
    s = min(FIXED_SCALE, FIT_HI / omax) if omax > 1e-9 else FIXED_SCALE
    try:
        scaled, stats = scale_code(src, scale=s, clamp=10 ** 9, min_mag=MIN_MAG)
    except SyntaxError as e:
        return {"error": f"parse: {e}", "stage": "scale"}
    sb, st2 = bbox(p, scaled)          # 2) 缩放后包围盒
    if sb is None:
        return {"error": st2, "stage": "scaled"}
    sxl, syl, szl, sxmin, symin, szmin = sb
    # 3) 忠实性: 每轴 缩放后 ≈ s×原始
    faithful = all(abs(sd - s * od) <= max(0.05 * s * od, 1.0)
                   for sd, od in ((sxl, oxl), (syl, oyl), (szl, ozl)) if od > 1e-6)
    if not faithful:
        return {"error": "unfaithful", "stage": "verify"}
    if max(sxl, syl, szl) > BOX_HI - BOX_LO + 1:
        return {"error": "too_big", "stage": "verify"}
    # 4) 用缩放后包围盒平移进 [1,10000]
    offs = []
    for mn, ln in ((sxmin, sxl), (symin, syl), (szmin, szl)):
        off = BOX_LO - mn
        if mn + ln + off > BOX_HI:
            off = BOX_HI - (mn + ln)
        offs.append(int(round(off)))
    final = scaled + f"\nresult = result.translate(({offs[0]}, {offs[1]}, {offs[2]}))\n"
    return {"scaled": final, "scale": s, "max_dim": omax,
            "offs": offs, "n_scaled": stats["n_scaled"]}


def worker_thread(tasks, results, progress):
    p = spawn(); n_since = 0
    while True:
        try:
            uuid, code = tasks.get_nowait()
        except queue.Empty:
            break
        d = process(p, code)
        # 任一次 bbox 超时/崩溃 -> 该 worker 可能已坏, 重启
        if d.get("stage") in ("orig", "scaled") and d.get("error") in ("timeout", "crash"):
            try: p.kill()
            except Exception: pass
            p = spawn(); n_since = 0
        results.append((uuid, code, d))
        progress[0] += 1; n_since += 1
        if n_since >= RECYCLE:
            try: p.kill()
            except Exception: pass
            p = spawn(); n_since = 0
    try: p.kill()
    except Exception: pass


def load_codes(indir, split, limit):
    out = []
    for f in sorted(glob.glob(os.path.join(indir, split, "*.parquet"))):
        t = pq.read_table(f, columns=["cadquery_file", "uuid"])
        col, uu = t.column("cadquery_file"), t.column("uuid")
        for i in range(t.num_rows):
            v = col[i].as_py()
            if isinstance(v, (bytes, bytearray)):
                v = bytes(v).decode("utf-8", "replace")
            out.append((uu[i].as_py(), v))
            if limit and len(out) >= limit:
                return out
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--indir", default="datasetquelle/Zero-To-CAD-100k/data")
    ap.add_argument("--outdir", default="Zero-To-CAD-Baseline/data/koor_box10k")
    ap.add_argument("--splits", nargs="*", default=["test"])
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()
    global TIMEOUT
    TIMEOUT = args.timeout

    for split in args.splits:
        codes = load_codes(args.indir, split, args.limit)
        if not codes:
            print(f"[{split}] 空, 跳过"); continue
        print(f"[{split}] {len(codes)} 模型 workers={args.workers} timeout={TIMEOUT}s", flush=True)
        tasks = queue.Queue()
        for c in codes:
            tasks.put(c)
        results = []; progress = [0]; t0 = time.time()
        threads = [threading.Thread(target=worker_thread, args=(tasks, results, progress))
                   for _ in range(args.workers)]
        for t in threads: t.start()
        while any(t.is_alive() for t in threads):
            time.sleep(10)
            n = progress[0]; rate = n / max(1e-6, time.time() - t0)
            print(f"  [{split}] {n}/{len(codes)} {rate:.1f}/s ETA {(len(codes)-n)/max(1e-6,rate)/60:.1f}min", flush=True)
        for t in threads: t.join()

        kept = {k: [] for k in ("uuid", "cadquery_file", "cadquery_file_orig",
                                "scale", "max_dim_mm", "offs", "n_scaled")}
        n_fail = Counter(); big = 0
        dropped = []
        for uuid, code, d in results:
            if "error" in d:
                n_fail[f"{d['stage']}:{d['error']}"] += 1
                dropped.append({"uuid": uuid, "code": code,
                                "stage": d.get("stage"), "error": d.get("error")})
                continue
            kept["uuid"].append(uuid)
            kept["cadquery_file"].append(d["scaled"])
            kept["cadquery_file_orig"].append(code)
            kept["scale"].append(float(d["scale"]))
            kept["max_dim_mm"].append(float(d["max_dim"]))
            kept["offs"].append(json.dumps(d["offs"]))
            kept["n_scaled"].append(int(d["n_scaled"]))
            if d["scale"] < 99.9: big += 1
        os.makedirs(args.outdir, exist_ok=True)
        tbl = pa.table({
            "uuid": pa.array(kept["uuid"], pa.string()),
            "cadquery_file": pa.array(kept["cadquery_file"], pa.string()),
            "cadquery_file_orig": pa.array(kept["cadquery_file_orig"], pa.string()),
            "scale": pa.array(kept["scale"], pa.float64()),
            "max_dim_mm": pa.array(kept["max_dim_mm"], pa.float64()),
            "offs": pa.array(kept["offs"], pa.string()),
            "n_scaled": pa.array(kept["n_scaled"], pa.int32()),
        })
        out = os.path.join(args.outdir, f"{split}.parquet")
        pq.write_table(tbl, out, compression="zstd")
        # 保存被丢弃的(含代码), 供恢复 pass 重试超时项
        with open(os.path.join(args.outdir, f"dropped_{split}.jsonl"), "w") as fp:
            for x in dropped:
                fp.write(json.dumps(x, ensure_ascii=False) + "\n")
        # 失败明细 top
        top = sorted(n_fail.items(), key=lambda x: -x[1])[:8]
        print(f"[{split}] 完成 kept={len(kept['uuid'])}/{len(codes)} big={big} "
              f"用时{(time.time()-t0)/60:.1f}min -> {out}", flush=True)
        print(f"[{split}] 失败明细: {dict(top)}", flush=True)


if __name__ == "__main__":
    main()
