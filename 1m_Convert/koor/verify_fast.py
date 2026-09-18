"""并行校验: 用常驻 bbox worker 执行 cadquery_file, 确认几何落在 [1,10000]。
用法: python verify_fast.py <parquet> [n] [workers]"""
import sys, os, json, random, subprocess, threading, queue, time
from collections import Counter
import pyarrow.parquet as pq
HERE = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 15
LO, HI = 1, 10000


# select.select() can't wait on pipes on Windows; use a reader thread + queue.
def spawn():
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    p = subprocess.Popen([sys.executable, os.path.join(HERE, "bbox_persistent.py")],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                         bufsize=1, encoding="utf-8", env=env)
    q = queue.Queue()

    def _pump():
        try:
            for line in p.stdout:
                q.put(line)
        except Exception:
            pass
        q.put(None)
    threading.Thread(target=_pump, daemon=True).start()
    p._outq = q
    try:
        p._outq.get(timeout=60)          # consume READY
    except queue.Empty:
        pass
    return p


def ask(p, code):
    try:
        p.stdin.write(json.dumps({"code": code}) + "\n"); p.stdin.flush()
    except Exception:
        return None
    try:
        line = p._outq.get(timeout=TIMEOUT)
    except queue.Empty:
        return None
    if line is None:
        return None
    try:
        return json.loads(line)
    except Exception:
        return None


def main():
    path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    W = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    t = pq.read_table(path, columns=["uuid", "cadquery_file", "scale", "max_dim_mm"])
    rng = random.Random(5)
    idxs = rng.sample(range(t.num_rows), min(n, t.num_rows))
    sc = t.column("cadquery_file"); uu = t.column("uuid"); scl = t.column("scale")
    tasks = queue.Queue()
    for i in idxs:
        tasks.put((uu[i].as_py(), sc[i].as_py(), scl[i].as_py()))
    results = []

    def wt():
        p = spawn()
        while True:
            try:
                uuid, code, s = tasks.get_nowait()
            except queue.Empty:
                break
            d = ask(p, code)
            if d is None:
                try: p.kill()
                except Exception: pass
                p = spawn(); d = {"error": "timeout"}
            results.append((uuid, s, d))
        try: p.kill()
        except Exception: pass

    th = [threading.Thread(target=wt) for _ in range(W)]
    for x in th: x.start()
    for x in th: x.join()

    tally = Counter(); bad = []
    for uuid, s, d in results:
        if "error" in d:
            tally["exec_fail"] += 1; continue
        xl, yl, zl, xmin, ymin, zmin = d["bb"]
        lo = min(xmin, ymin, zmin); hi = max(xmin + xl, ymin + yl, zmin + zl)
        if lo >= LO - 0.6 and hi <= HI + 0.6:
            tally["in_box"] += 1
        else:
            tally["out_of_box"] += 1
            bad.append((uuid, f"[{lo:.1f},{hi:.1f}] scale={s:.2f}"))
    print(f"=== 校验 {len(results)} 个 (盒子[{LO},{HI}]) ===")
    for k, v in tally.most_common():
        print(f"  {k:12s} {v}")
    for u, info in bad[:15]:
        print(f"  OUT {u}: {info}")
    ib = tally["in_box"]; tot = ib + tally["out_of_box"]
    print(f"\n落盒率: {ib}/{tot}" + (f" = {100*ib/tot:.1f}%" if tot else ""))


if __name__ == "__main__":
    main()
