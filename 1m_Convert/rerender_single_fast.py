"""单件装配统一重渲染(常驻 worker 版, 快): 对已存在的 *__asm 目录, 用最新
assemble_fasteners/drawing 代码重出图(螺钉头顶锚点+可读标题+气泡/ISO/角度修复)。

提速同 rerender_two_fast: Pool(每 worker 只 import 一次 + 建一次 uuid->code
索引) + produce(rerender_only=True)(强制光杆紧固件跳过带螺纹建模 4.8s/个 +
跳 model.step 重导出 + skip verify)。几何确定性不变, 只覆盖 drawing。

用法: python -X utf8 rerender_single_fast.py [--jobs N] [--limit N] [--only-old]
"""
import sys, os, glob, argparse, time
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTDIR = os.path.join(HERE, "assemblies")

_W = {}


def _winit():
    sys.path.insert(0, ROOT)
    sys.path.insert(0, HERE)
    import cadquery as cq
    import pyarrow.parquet as pq
    import assemble_fasteners as af
    from types import SimpleNamespace
    import math
    _W["af"] = af
    _W["cq"] = cq
    _W["ns"] = SimpleNamespace
    _W["math"] = math
    idx = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "test", "*.parquet"))):
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            for row in pf.read_row_group(
                    rg, columns=["uuid", "cadquery_file"]).to_pylist():
                idx[row["uuid"]] = row["cadquery_file"]
    _W["idx"] = idx


def _exec_part(code):
    cq = _W["cq"]
    if isinstance(code, (bytes, bytearray)):
        code = bytes(code).decode("utf-8", "replace")
    g = {"cq": cq, "SimpleNamespace": _W["ns"], "math": _W["math"], "__name__": "x"}
    exec(code, g)
    r = g.get("result")
    if r is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                r = v
    return r, code


def _do(task):
    """task=(uuid, name, fastener). 返回 (name, status)."""
    uuid, name, fastener = task
    af = _W["af"]
    idx = _W["idx"]
    try:
        code = idx.get(uuid)
        if code is None:
            return (name, "NOSRC")
        shape, code = _exec_part(code)
        if shape is None:
            return (name, "NOSHAPE")
        res = af.produce(shape, name, OUTDIR, fastener=fastener,
                         add_washer=True, add_nut=True, part_source=code,
                         rerender_only=True)
        if res is None:
            return (name, "NORES")
        return (name, "OK")
    except Exception as e:
        return (name, "ERR:" + type(e).__name__)


def _is_old(d):
    """标题区还是旧/缺失 -> 需重渲染。新规则标题形如 'M4 socket assembly'。"""
    svg = os.path.join(d, "drawing.svg")
    if not os.path.isfile(svg):
        return True
    try:
        with open(svg, encoding="utf-8", errors="ignore") as fh:
            t = fh.read()
        return " assembly" not in t      # 可读装配标题缺失 = 旧
    except Exception:
        return True


def _parse(name):
    uuid = name.split("__")[0]
    fastener = "hex" if name[:-len("__asm")].endswith("_hex") else "socket"
    return uuid, fastener


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only-old", action="store_true")
    args = ap.parse_args()

    tasks, skip_have = [], 0
    for d in sorted(glob.glob(os.path.join(OUTDIR, "*__asm"))):
        if not os.path.isdir(d):
            continue
        if args.only_old and not _is_old(d):
            skip_have += 1
            continue
        name = os.path.basename(d)
        uuid, fastener = _parse(name)
        tasks.append((uuid, name, fastener))
        if args.limit and len(tasks) >= args.limit:
            break

    print(f"单件重渲染清单: {len(tasks)} 件; 跳过(已新) {skip_have}; "
          f"jobs={args.jobs}", flush=True)
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
                # 新判据下装不上(NORES/干涉/坏几何) -> 删旧目录, 不留过时图
                shutil.rmtree(os.path.join(OUTDIR, name), ignore_errors=True)
                cnt["DEL"] += 1
            if cnt["n"] % 25 == 0:
                el = time.time() - t0
                rate = cnt["n"] / el if el else 0
                eta = (len(tasks) - cnt["n"]) / rate if rate else 0
                print(f"  进度 {cnt['n']}/{len(tasks)} ok{cnt['OK']} del{cnt['DEL']} "
                      f"  {rate:.2f}件/s ETA {eta/60:.1f}min", flush=True)
    el = time.time() - t0
    print(f"\n单件重渲染完成: ok {cnt['OK']}, 删除 {cnt['DEL']} / {len(tasks)}  "
          f"用时 {el/60:.1f}min  ({cnt['n']/max(el,1e-9):.2f}件/s)", flush=True)


if __name__ == "__main__":
    main()
