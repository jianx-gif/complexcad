"""给已产出但缺 svg/dxf 的双件装配补出三格式工程图(png+svg+dxf)。

做法: 解析子目录名 <uuidA8>_<uuidB8>__<Mtag>__two -> 用候选池缓存(two_pool.json)
把 8 位前缀还原成完整 uuid -> 调 produce_two_one 子进程(它产三格式, 覆盖原产出)。
装配几何**完全确定性**(同一对件 + 同一配对/对齐算法 => 同一结果), 故覆盖不会改变
已验证好的几何, 只是补上 svg/dxf。

只处理缺 drawing.svg 或 drawing.dxf 的件; 已齐的跳过。并行 jobs 路, 单件超时。
用法: python -X utf8 backfill_two.py [--jobs 8] [--timeout 300]
"""
import os, sys, json, glob, argparse, subprocess, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "two_part_assemblies")
SCRATCH = os.environ.get("CLAUDE_SCRATCH", HERE)
POOL_CACHE = os.path.join(SCRATCH, "two_pool.json")


def _prefix_map():
    """8位前缀 -> 完整 uuid 映射。优先候选池缓存; 缺失则扫 test parquet 全量 uuid。"""
    m = {}
    try:
        pool = json.load(open(POOL_CACHE, encoding="utf-8"))
        for e in pool:
            for _p in (e["uuid"][:8], e["uuid"][:12]):
                m[_p] = e["uuid"]
    except Exception:
        pass
    if not m:                                     # 缓存缺失: 从 test parquet 兜底
        try:
            import glob as _glob
            import pyarrow.parquet as _pq
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            for f in sorted(_glob.glob(os.path.join(root, "test", "*.parquet"))):
                pf = _pq.ParquetFile(f)
                for rg in range(pf.num_row_groups):
                    for row in pf.read_row_group(rg, columns=["uuid"]).to_pylist():
                        for _p in (row["uuid"][:8], row["uuid"][:12]):
                            m[_p] = row["uuid"]
        except Exception:
            pass
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--all", action="store_true", help="全部重跑(不跳过已齐), 应用最新代码")
    args = ap.parse_args()

    pmap = _prefix_map()
    todo = []          # (uuidA, uuidB, name)
    skip_have = 0
    skip_noresolve = 0
    for d in sorted(glob.glob(os.path.join(OUTDIR, "*__two"))):
        name = os.path.basename(d)
        if not os.path.isfile(os.path.join(d, "drawing.png")):
            continue
        # "已齐" = 装配图三格式 + 装配 stl + partA/partB(各含 drawing.png/svg/dxf +
        # model.step + model.stl)。任一缺失则重跑 produce_two 补齐(确定性, 不改几何)。
        def _full(sub=""):
            p = os.path.join(d, sub) if sub else d
            need = ["drawing.png", "drawing.svg", "drawing.dxf", "model.step",
                    "model.stl"]
            if sub:
                need.append("cadquery.py")
            return all(os.path.isfile(os.path.join(p, f)) for f in need)
        if ("--all" not in sys.argv) and _full() and _full("partA") and _full("partB"):
            skip_have += 1
            continue
        # 名字: <A8>_<B8>__<Mtag>__two
        base = name.split("__")[0]
        if "_" not in base:
            continue
        a8, b8 = base.split("_", 1)
        ua, ub = pmap.get(a8), pmap.get(b8)
        if ua is None or ub is None:
            skip_noresolve += 1
            print(f"  [无法还原 uuid] {name} (a8={a8} b8={b8})", flush=True)
            continue
        todo.append((ua, ub, name))

    print(f"补图清单: {len(todo)} 件; 已齐 {skip_have}; 无法还原 {skip_noresolve}",
          flush=True)
    if not todo:
        return

    lock = threading.Lock()
    cnt = {"ok": 0, "fail": 0}

    def run(item):
        ua, ub, name = item
        try:
            cp = subprocess.run(
                [sys.executable, "-X", "utf8",
                 os.path.join(HERE, "produce_two_one.py"), ua, ub, name],
                cwd=HERE, timeout=args.timeout, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            with lock:
                cnt["fail"] += 1
                import shutil
                shutil.rmtree(os.path.join(OUTDIR, name), ignore_errors=True)
                cnt["deleted"] = cnt.get("deleted", 0) + 1
                print(f"  [TIMEOUT->DEL] {name}", flush=True)
            return
        ok = cp.returncode == 0 and "OK" in (cp.stdout or "")
        with lock:
            if ok:
                cnt["ok"] += 1
                if cnt["ok"] % 20 == 0:
                    print(f"  补图进度 {cnt['ok']}/{len(todo)}", flush=True)
            else:
                cnt["fail"] += 1
                tail = (cp.stdout or "").strip().splitlines()[-1:] or [""]
                # 新判据下该对装不成有效双件(NOPAIR/NORES/干涉) -> 删旧目录,
                # 不留旧图(它不该在双件数据集里)。
                import shutil
                shutil.rmtree(os.path.join(OUTDIR, name), ignore_errors=True)
                cnt["deleted"] = cnt.get("deleted", 0) + 1
                print(f"  [DEL] {name} rc={cp.returncode} {tail[-1][:40]}",
                      flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(run, it) for it in todo]
        for _ in as_completed(futs):
            pass
    print(f"\n双件重跑完成: 成功 {cnt['ok']}, 失败 {cnt['fail']} "
          f"(其中删除 {cnt.get('deleted', 0)})", flush=True)


if __name__ == "__main__":
    main()
