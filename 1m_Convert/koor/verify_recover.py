"""验证量化代码可无损还原 (转换脚本的核心价值证明)。

对 output_koor/<uuid>/ 每个模型:
  1. 执行 cadquery.py            -> 原始几何 bbox  (真实 mm)
  2. 执行 koor.json.conv_code    -> 量化几何 bbox  (落在 [1,10000] 盒)
  3. 反变换 (bbox - offs) / scale -> 还原 bbox
  4. 对比 还原 vs 原始: 每轴长度误差应 <= 1/scale (量化网格), 即 <=0.01mm@scale100

输出每模型误差 + 全体统计 (max/mean 误差, 落在网格内的比例)。
用法: python verify_recover.py [N]
"""
import sys, os, glob, json, subprocess, threading, queue
import pyarrow.parquet as pq  # noqa (kept for parity / future parquet read)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output_koor")
TIMEOUT = 90


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
        p._outq.get(timeout=60)
    except queue.Empty:
        pass
    return p


def bbox(p, code):
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
        d = json.loads(line)
    except Exception:
        return None
    return d.get("bb")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    dirs = sorted(glob.glob(os.path.join(OUT, "*", "")))
    if n:
        dirs = dirs[:n]
    p = spawn()
    rows = []
    for d in dirs:
        u = os.path.basename(os.path.normpath(d))
        try:
            orig_code = open(os.path.join(d, "cadquery.py"), encoding="utf-8").read()
            kd = json.load(open(os.path.join(d, "koor.json"), encoding="utf-8"))
        except Exception as e:
            rows.append((u, None, f"read: {e}")); continue
        scale = kd["scale"]
        offs = json.loads(kd["offs"]) if isinstance(kd["offs"], str) else kd["offs"]
        conv_code = kd["conv_code"]

        ob = bbox(p, orig_code)
        if ob is None:
            p.kill(); p = spawn()
            rows.append((u, None, "orig exec fail/timeout")); continue
        cb = bbox(p, conv_code)
        if cb is None:
            p.kill(); p = spawn()
            rows.append((u, None, "conv exec fail/timeout")); continue
        # bb = [xl, yl, zl, xmin, ymin, zmin]; lengths are scale-only (offset-free)
        # recovered length = quantized length / scale
        rec_len = [cb[i] / scale for i in range(3)]
        err = [abs(rec_len[i] - ob[i]) for i in range(3)]
        max_err = max(err)
        rows.append((u, max_err, f"orig={[round(x,2) for x in ob[:3]]} "
                                 f"rec={[round(x,2) for x in rec_len]}"))
    p.kill()

    print(f"=== 量化还原验证 ({len(rows)} 模型, scale 网格 ~0.01mm) ===")
    ok = bad = fail = 0
    errs = []
    for u, e, info in rows:
        if e is None:
            fail += 1
            print(f"  FAIL {u[:8]} {info}")
            continue
        errs.append(e)
        tag = "OK " if e <= 0.011 else "DIFF"
        if e <= 0.011:
            ok += 1
        else:
            bad += 1
            print(f"  {tag} {u[:8]} max_err={e:.4f}mm  {info}")
    if errs:
        print(f"\n还原误差: max={max(errs):.4f}mm  mean={sum(errs)/len(errs):.5f}mm")
    print(f"网格内(<=0.011mm): {ok}/{ok+bad}  超差: {bad}  执行失败: {fail}")


if __name__ == "__main__":
    main()
