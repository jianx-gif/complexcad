"""双件统一重渲染(常驻 worker 版, 快): 对已存在的 *__two 目录, 用最新
assemble_two/drawing 代码重出图(头顶锚点+可读标题+气泡/ISO 修复)。

为什么快: 旧法每张图 spawn 一个 produce_two_one 子进程, 每次都付
`import cadquery`(OCP/OCCT 内核加载 ~20-47s) + 重扫 3.2G parquet 找 uuid 的税。
本脚本用 multiprocessing.Pool: 每个 worker **只 import 一次 + 只建一次
uuid->code 索引(仅读两列, ~14MB 常驻)**, 然后串行连出多张图。import 税从
"每张一次"摊成"每 worker 一次"。几何确定性不变(同源+同算法=同结果),
只是覆盖旧图。装不成的对(NOPAIR/VERIFY/NORES)删目录, 不留旧图。

用法: python -X utf8 rerender_two_fast.py [--jobs N] [--limit N] [--only-old]
  --only-old: 只重渲染"标题还不是 two-part assembly"的旧图(跳过已是新规则的)
"""
import sys, os, glob, json, argparse, time
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTDIR = os.path.join(HERE, "two_part_assemblies")
SCRATCH = os.environ.get("CLAUDE_SCRATCH", HERE)

# ---- worker 全局(每进程一次) ----
_W = {}


def _winit():
    """每个 worker 启动一次: import 重内核 + 建 uuid->code 索引。"""
    sys.path.insert(0, ROOT)
    sys.path.insert(0, HERE)
    import cadquery  # noqa: 触发 OCP 加载一次
    import pyarrow.parquet as pq
    import assemble_two as a2
    _W["a2"] = a2
    idx = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "test", "*.parquet"))):
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            for row in pf.read_row_group(
                    rg, columns=["uuid", "cadquery_file"]).to_pylist():
                idx[row["uuid"]] = row["cadquery_file"]
    _W["idx"] = idx
    _W["pre8"] = {p: u for u in idx for p in (u[:8], u[:12])}  # 8/12位前缀均可解析


def _resolve(p8):
    return _W["pre8"].get(p8)


def _do(task):
    """task=(uA, uB, name, fastener). 返回 (name, status)."""
    uA, uB, name, fastener = task
    a2 = _W["a2"]
    idx = _W["idx"]
    try:
        cA, cB = idx.get(uA), idx.get(uB)
        if cA is None or cB is None:
            return (name, "NOSRC")
        shapeA, srcA = a2.exec_part(cA)
        shapeB, srcB = a2.exec_part(cB)
        if shapeA is None or shapeB is None:
            return (name, "NOSHAPE")
        # 不预调 assemble_two/verify_geometry(produce_two 内部会装配); 传
        # skip_verify=True 跳过最贵的布尔相交校验(几何已验证过)。srcA/srcB
        # 仍传入以重生成 assembly 脚本与零件详图(用新代码)。
        out = a2.produce_two(shapeA, shapeB, name, OUTDIR, fastener,
                             srcA, srcB, fmts=("png", "svg", "dxf"),
                             rerender_only=True)
        if out is None:
            return (name, "NORES")
        return (name, "OK")
    except Exception as e:
        return (name, "ERR:" + type(e).__name__)


def _is_old(d):
    """标题还不是新规则(不含 'two-part assembly')-> 需重渲染。"""
    svg = os.path.join(d, "drawing.svg")
    if not os.path.isfile(svg):
        return True
    try:
        with open(svg, encoding="utf-8", errors="ignore") as fh:
            return "two-part assembly" not in fh.read(6000)
    except Exception:
        return True


def _build_tasks(only_old, limit):
    # 8位前缀映射(主进程也需要一份来解析目录名)
    pre8 = {}
    try:
        pool = json.load(open(os.path.join(SCRATCH, "two_pool.json"),
                              encoding="utf-8"))
        for e in pool:
            for _p in (e["uuid"][:8], e["uuid"][:12]):
                pre8[_p] = e["uuid"]
    except Exception:
        pass
    # 始终用全量 parquet 补全 pre8(two_pool.json 不含全部 uuid, 漏的会"无法还原")
    import pyarrow.parquet as pq
    for f in sorted(glob.glob(os.path.join(ROOT, "test", "*.parquet"))):
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            for row in pf.read_row_group(rg, columns=["uuid"]).to_pylist():
                for _p in (row["uuid"][:8], row["uuid"][:12]):
                    pre8.setdefault(_p, row["uuid"])
    tasks, skip_have, skip_noresolve = [], 0, 0
    for d in sorted(glob.glob(os.path.join(OUTDIR, "*__two"))):
        name = os.path.basename(d)
        if only_old and not _is_old(d):
            skip_have += 1
            continue
        base = name.split("__")[0]
        if "_" not in base:
            continue
        a8, b8 = base.split("_", 1)
        uA, uB = pre8.get(a8), pre8.get(b8)
        if uA is None or uB is None:
            skip_noresolve += 1
            continue
        tasks.append((uA, uB, name, "socket"))
        if limit and len(tasks) >= limit:
            break
    return tasks, skip_have, skip_noresolve


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only-old", action="store_true")
    ap.add_argument("--names-file", default=None,
                    help="只重渲染该文件里列出的目录名(每行一个), 精准补渲染")
    args = ap.parse_args()

    tasks, skip_have, skip_noresolve = _build_tasks(args.only_old, args.limit)
    if args.names_file:
        want = set(l.strip() for l in open(args.names_file, encoding="utf-8")
                   if l.strip())
        tasks = [t for t in tasks if t[2] in want]  # t=(uA,uB,name,fastener)
        print(f"[names-file] 过滤到 {len(tasks)} 件(清单 {len(want)})", flush=True)
    print(f"重渲染清单: {len(tasks)} 件; 跳过(已新) {skip_have}; "
          f"无法还原 {skip_noresolve}; jobs={args.jobs}", flush=True)
    if not tasks:
        print("无待办, 退出。", flush=True)
        return

    import shutil
    t0 = time.time()
    cnt = {"OK": 0, "DEL": 0, "n": 0}
    with mp.Pool(args.jobs, initializer=_winit) as pool:
        for name, st in pool.imap_unordered(_do, tasks, chunksize=1):
            cnt["n"] += 1
            if st == "OK":
                cnt["OK"] += 1
            else:
                # 装不成 -> 删旧目录, 不留过时/无效图
                shutil.rmtree(os.path.join(OUTDIR, name), ignore_errors=True)
                cnt["DEL"] += 1
            if cnt["n"] % 25 == 0:
                el = time.time() - t0
                rate = cnt["n"] / el if el else 0
                eta = (len(tasks) - cnt["n"]) / rate if rate else 0
                print(f"  进度 {cnt['n']}/{len(tasks)} ok{cnt['OK']} del{cnt['DEL']} "
                      f"  {rate:.2f}件/s ETA {eta/60:.1f}min", flush=True)
    el = time.time() - t0
    print(f"\n双件重渲染完成: ok {cnt['OK']}, 删除 {cnt['DEL']} / {len(tasks)}  "
          f"用时 {el/60:.1f}min  ({cnt['n']/el:.2f}件/s)", flush=True)


if __name__ == "__main__":
    main()
