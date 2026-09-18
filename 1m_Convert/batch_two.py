"""批量生成双件夹紧装配(目标 1000 个), 关键: 两件之间不干涉、平面对接贴合。

流程:
  阶段1(候选池, 可缓存): 扫描数据集, 对每个件检孔, 并判定每个孔的"平面对接端"
    (规格 + 顶/底端口是否垂直于轴的平面 + 孔位)。只收录"至少有一个平面对接孔"的件。
  阶段2(配对): 按螺纹规格分组, 组内两两配对(优选孔径接近、孔间距 pattern 接近),
    生成待做清单(命名 <uuidA8>_<uuidB8>__<Mtag>__two, 跳过已存在)。
  阶段3(并行产出): {jobs} 路子进程跑 produce_two_one, 每件带超时; 内部装配 +
    A-B 干涉检查 + verify_geometry, 通过才落盘。攒到 N 个成功为止。

用法: python -X utf8 batch_two.py [N] [--jobs 12] [--timeout 240] [--scan 3000]
"""
import sys, os, glob, json, argparse, subprocess, shutil, math, threading
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import cadquery as cq
from types import SimpleNamespace
import pyarrow.parquet as pq
import assemble_fasteners as af
import assemble_two as a2
from concurrent.futures import ThreadPoolExecutor, as_completed

import dataset_source  # 数据源经环境变量传给 worker 子进程
OUTDIR = os.path.join(HERE, "two_part_assemblies")
SCRATCH = os.environ.get("CLAUDE_SCRATCH", HERE)
POOL_CACHE = os.path.join(SCRATCH, "two_pool.json")


def _parse_chunk_stdout(text):
    """从 scan_two_chunk 的 stdout 解析候选行。返回 [entry...]。"""
    out = []
    for ln in (text or "").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("__DONE__"):
            continue
        try:
            e = json.loads(ln)
            if "uuid" in e and "holes" in e:
                out.append(e)
        except Exception:
            pass
    return out


def build_pool(target_parts, scan_limit, jobs, chunk=60, chunk_timeout=120):
    """扫描数据集建候选池(子进程分块 + 超时, 病态件不拖死)。返回 list of {uuid,holes}.
    每个 chunk 子进程扫 `chunk` 个件, 超时则只取它在超时前已打印的候选(部分结果)。
    缓存到 POOL_CACHE。攒够 target_parts 即停止派发新 chunk。"""
    if os.path.isfile(POOL_CACHE):
        try:
            pool = json.load(open(POOL_CACHE, encoding="utf-8"))
            if len(pool) >= target_parts:
                print(f"[pool] 复用缓存 {POOL_CACHE}: {len(pool)} 件", flush=True)
                return pool
            print(f"[pool] 缓存仅 {len(pool)} < {target_parts}, 重新扫描", flush=True)
        except Exception:
            pass
    pool = []
    seen_uuids = set()
    lock = threading.Lock()
    starts = list(range(0, scan_limit, chunk))
    stop = {"v": False}

    def run_chunk(start):
        if stop["v"]:
            return []
        try:
            cp = subprocess.run(
                [sys.executable, "-X", "utf8",
                 os.path.join(HERE, "scan_two_chunk.py"), str(start), str(chunk)],
                cwd=HERE, timeout=chunk_timeout, capture_output=True, text=True)
            txt = cp.stdout
        except subprocess.TimeoutExpired as te:
            txt = te.stdout.decode("utf-8", "replace") if isinstance(
                te.stdout, (bytes, bytearray)) else (te.stdout or "")
        return _parse_chunk_stdout(txt)

    with ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(run_chunk, s): s for s in starts}
        for fut in as_completed(futs):
            entries = fut.result()
            with lock:
                for e in entries:
                    if e["uuid"] in seen_uuids:
                        continue
                    seen_uuids.add(e["uuid"])
                    pool.append(e)
                if len(pool) >= target_parts:
                    stop["v"] = True
                print(f"[pool] 候选 {len(pool)}/{target_parts} "
                      f"(chunk@{futs[fut]} +{len(entries)})", flush=True)
    print(f"[pool] 完成: 候选 {len(pool)} 件", flush=True)
    try:
        json.dump(pool, open(POOL_CACHE, "w", encoding="utf-8"))
    except Exception:
        pass
    return pool


def make_pairs(pool, target_pairs, max_reuse=0):
    """按规格分组配对。A 需提供平面顶端(hi)、B 需平面底端(lo)。
    组内按孔径接近排序两两配。返回 [(uuidA, uuidB, mtag)] 候选(留余量)。

    max_reuse>0: 限制单个零件(不分 A/B, 跨规格合计)最多参与几对。避免少数
    "有规整通孔"的枢纽件被贪心最近邻反复配上去霸屏(实测未限制时单件可占 25%),
    从而提升整批装配的零件多样性。0 = 不限(旧行为)。达上限的零件从后续配对中
    退出, 让位给孔径次相近但未用尽的零件, 故需要更大的候选池(调大 --scan)才能
    在收紧上限的同时凑够 target_pairs。"""
    from collections import Counter
    # 收集每件能做 A(有 hi 平面孔) / 做 B(有 lo 平面孔) 的孔规格
    by_size_A = {}  # size -> [(uuid, r)]
    by_size_B = {}
    for e in pool:
        for h in e["holes"]:
            if h["hi"]:
                by_size_A.setdefault(h["size"], []).append((e["uuid"], h["r"]))
            if h["lo"]:
                by_size_B.setdefault(h["size"], []).append((e["uuid"], h["r"]))
    pairs = []
    used = set()
    use_count = Counter()          # uuid -> 已参与配对次数(A/B 合计)

    def capped(u):
        return max_reuse > 0 and use_count[u] >= max_reuse

    sizes = sorted(set(by_size_A) & set(by_size_B))
    # 优先孔径接近: 把 A、B 候选各按 r 排序, 贪心配相近的
    for size in sizes:
        As = sorted(by_size_A.get(size, []), key=lambda x: x[1])
        Bs = sorted(by_size_B.get(size, []), key=lambda x: x[1])
        mtag = "M" + size.split("-")[0].lstrip("M")
        for (ua, ra) in As:
            if capped(ua):                     # A 已用尽复用额度, 跳过
                continue
            # 找一个 r 最接近、且不等于 ua、未配过、未达复用上限的 B
            best = None
            for j in range(len(Bs)):
                ub, rb = Bs[j]
                if ub == ua or capped(ub):
                    continue
                key = tuple(sorted((ua, ub))) + (size,)
                if key in used:
                    continue
                err = abs(ra - rb)
                if best is None or err < best[0]:
                    best = (err, j, ub, key)
            if best is None:
                continue
            _, j, ub, key = best
            used.add(key)
            use_count[ua] += 1
            use_count[ub] += 1
            pairs.append((ua, ub, mtag))
            if len(pairs) >= target_pairs:
                return pairs
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", nargs="?", type=int, default=1000)
    ap.add_argument("--jobs", type=int, default=12)
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--scan", type=int, default=4000, help="阶段1最多扫描多少个件")
    ap.add_argument("--pool", type=int, default=0,
                    help="候选池目标件数(默认 = max(800, 2*n 的一半余量))")
    ap.add_argument("--max-reuse", type=int, default=3,
                    help="单个零件最多参与几对(提升装配多样性, 避免枢纽件霸屏); "
                         "0=不限。收紧此值需相应调大 --scan 才能凑够目标数")
    ap.add_argument("--fastener", default="socket", choices=["socket", "hex"])
    args = ap.parse_args()
    os.makedirs(OUTDIR, exist_ok=True)

    pool_target = args.pool or max(900, int(args.n * 0.9))
    pool = build_pool(pool_target, args.scan, args.jobs)

    # 预建 uuid->源码缓存: 让 produce_two_one 子进程查表取零件源码, 免每配一对都
    # 线性重扫 parquet(多 worker 并发扫同一批 parquet 会严重 I/O 争抢, 是生成慢的
    # 主因)。失败不影响正确性——produce_two_one 缺缓存会自动回退扫 parquet。
    try:
        import build_src_cache
        build_src_cache.build_cache([e["uuid"] for e in pool])
    except Exception as e:
        print("[cache] 预建跳过(worker将回退扫parquet): %s: %s"
              % (type(e).__name__, e), flush=True)

    # 配对留大余量: A-B 干涉/平面/完整孔筛选会刷掉约 70%, 故按 ~5x 目标生成候选对。
    pairs = make_pairs(pool, int(args.n * 5), max_reuse=args.max_reuse)
    n_parts = len({u for p in pairs for u in p[:2]})
    print(f"[pair] 生成候选配对 {len(pairs)} 对, 涉及 {n_parts} 个不同零件 "
          f"(复用上限 {args.max_reuse or '∞'})", flush=True)

    # 过滤已存在
    worklist = []
    done = 0
    for ua, ub, mtag in pairs:
        # 12 位前缀: 980k 规模下 8 位有生日碰撞(期望~110对), 12 位期望~0。
        name = f"{ua[:12]}_{ub[:12]}__{mtag}__two"
        if os.path.isfile(os.path.join(OUTDIR, name, "drawing.png")):
            done += 1
            continue
        worklist.append((ua, ub, name))
    print(f"[pair] 已存在 {done}, 待做 {len(worklist)}", flush=True)

    counter = {"made": done, "fail": 0, "intf": 0}
    lock = threading.Lock()
    target = args.n
    stop = {"v": False}

    def run_one(item):
        if stop["v"]:
            return
        ua, ub, name = item
        with lock:
            if counter["made"] >= target:
                stop["v"] = True
                return
        try:
            cp = subprocess.run(
                [sys.executable, "-X", "utf8",
                 os.path.join(HERE, "produce_two_one.py"), ua, ub, name,
                 args.fastener],
                cwd=HERE, timeout=args.timeout, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            shutil.rmtree(os.path.join(OUTDIR, name), ignore_errors=True)
            with lock:
                counter["fail"] += 1
            return
        if cp.returncode != 0 or "OK" not in (cp.stdout or ""):
            shutil.rmtree(os.path.join(OUTDIR, name), ignore_errors=True)
            with lock:
                counter["fail"] += 1
                if "VERIFY_FAIL" in (cp.stdout or ""):
                    counter["intf"] += 1
                if counter["fail"] <= 25:
                    tail = (cp.stdout or "").strip().splitlines()[-1:] or [""]
                    print(f"  [FAIL] {name} rc={cp.returncode} {tail[-1][:50]}",
                          flush=True)
            return
        with lock:
            counter["made"] += 1
            if counter["made"] % 25 == 0:
                print(f"  进度 {counter['made']}/{target} "
                      f"(失败 {counter['fail']}, 含校验/干涉 {counter['intf']})",
                      flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(run_one, it) for it in worklist]
        for _ in as_completed(futs):
            if counter["made"] >= target:
                stop["v"] = True

    print(f"\n完成: 成功 {counter['made']}/{target}  失败 {counter['fail']} "
          f"(含校验/干涉失败 {counter['intf']})  -> {OUTDIR}", flush=True)


if __name__ == "__main__":
    main()
