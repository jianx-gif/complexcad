"""批量装配 1000 件: 从 test 数据集取真实毫米零件 -> 检孔 -> 装配螺钉+垫圈+
螺母全套 -> 出三视图。命名 = <零件名/uuid前段>__<主螺钉规格>__set。

只收录"检出可匹配孔"的零件; 没有合适孔的跳过, 直到攒够 N 件。
输出隔离: 1m_Convert/assemblies/<name>/  (cadquery源/step/stl/三视图/assembly.json)
用法: python batch_assemble.py [N] [--fastener socket|hex]
"""
import sys, os, glob, json, argparse, traceback, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import cadquery as cq
from types import SimpleNamespace
import math
import pyarrow.parquet as pq
import assemble_fasteners as af
import make_drawings as md

OUTDIR = os.path.join(HERE, "assemblies")
import dataset_source  # 数据源: Z2C_PARQUET_GLOB / Z2C_SHARD 可配(默认 test/)


def exec_part(code):
    if isinstance(code, (bytes, bytearray)):
        code = bytes(code).decode("utf-8", "replace")
    g = {"cq": cq, "SimpleNamespace": SimpleNamespace, "math": math, "__name__": "x"}
    exec(code, g)
    r = g.get("result")
    if r is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                r = v
    return r, code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", nargs="?", type=int, default=1000)
    ap.add_argument("--fastener", default="socket", choices=["socket", "hex"])
    ap.add_argument("--offset", type=int, default=0, help="跳过前 offset 个候选")
    ap.add_argument("--timeout", type=int, default=300,
                    help="单件超时秒数(超时跳过, 防病态零件拖死批量)")
    ap.add_argument("--jobs", type=int, default=12,
                    help="并行 worker 数(子进程并发)")
    args = ap.parse_args()
    os.makedirs(OUTDIR, exist_ok=True)

    import shutil
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading

    files = dataset_source.parquet_files()

    # ===== 阶段1(串行, 快): 扫描候选, 做孔探测+命名+跳过已存在, 攒出待做清单 =====
    # 已完成件直接计入 done; 没合适孔的跳过。攒到 n 个"已完成或待做"为止。
    seen = 0
    skipped_nohole = 0
    fail = 0
    done = 0                       # 已存在(复用)的件数
    worklist = []                  # [(uuid, name)] 待 produce
    target = args.n
    for f in files:
        if done + len(worklist) >= target:
            break
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            if done + len(worklist) >= target:
                break
            tbl = pf.read_row_group(rg, columns=["uuid", "cadquery_file"]).to_pylist()
            for row in tbl:
                if done + len(worklist) >= target:
                    break
                seen += 1
                if seen <= args.offset:
                    continue
                uuid = row["uuid"]
                try:
                    shape, code = exec_part(row["cadquery_file"])
                    if shape is None:
                        fail += 1
                        continue
                    holes = af.cylinder_holes(shape)
                    matches = [af.match_screw_size(2 * h[0]) for h in holes]
                    matches = [m for m in matches if m]
                    if not matches:
                        skipped_nohole += 1
                        continue
                    sizes = [m[0] for m in matches]
                    mn = max(set(sizes), key=sizes.count)
                    tag = mn.split("-")[0]
                    name = f"{uuid}__{tag}_{args.fastener}__asm"
                    if os.path.isfile(os.path.join(OUTDIR, name, "drawing.png")):
                        done += 1                      # 已存在, 复用
                        continue
                    worklist.append((uuid, name))
                except Exception as e:
                    fail += 1
                    if fail <= 10:
                        print(f"  [FAIL] {uuid[:8]} {type(e).__name__}: "
                              f"{str(e)[:70]}", flush=True)
    print(f"阶段1: 已存在 {done}, 待做 {len(worklist)}, 无孔跳过 {skipped_nohole}, "
          f"探测失败 {fail}", flush=True)

    # ===== 阶段2(并行): 用 {jobs} 路子进程跑 produce_one, 每件带超时 =====
    lock = threading.Lock()
    counter = {"made": done, "fail": fail}

    def run_one(item):
        uuid, name = item
        try:
            cp = subprocess.run(
                [sys.executable, "-X", "utf8",
                 os.path.join(HERE, "produce_one.py"), uuid, name, args.fastener],
                cwd=HERE, timeout=args.timeout, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            shutil.rmtree(os.path.join(OUTDIR, name), ignore_errors=True)
            with lock:
                counter["fail"] += 1
                print(f"  [TIMEOUT>{args.timeout}s] {uuid[:8]} 跳过", flush=True)
            return
        if cp.returncode != 0 or "OK" not in (cp.stdout or ""):
            shutil.rmtree(os.path.join(OUTDIR, name), ignore_errors=True)
            with lock:
                counter["fail"] += 1
                if counter["fail"] <= 20:
                    err = (cp.stderr.strip().splitlines()[-1:] or [""])[-1]
                    print(f"  [FAIL] {uuid[:8]} rc={cp.returncode} {err[:60]}", flush=True)
            return
        with lock:
            counter["made"] += 1
            if counter["made"] % 25 == 0:
                print(f"  进度 {counter['made']}/{target}  "
                      f"(失败 {counter['fail']})", flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(run_one, it) for it in worklist]
        for _ in as_completed(futs):
            pass

    print(f"\n完成: 装配 {counter['made']} 件  扫描 {seen}  无合适孔 {skipped_nohole}  "
          f"失败 {counter['fail']}  -> {OUTDIR}", flush=True)


if __name__ == "__main__":
    main()
