"""双件装配 worker(子进程, 被 batch_two 以超时方式调用): 给两个 uuid + name,
从 test parquet 取两件源码、做平面对接装配 + A-B 干涉检查 + 出图产出。
成功打印 'OK' 退出 0; 失败/干涉/不可配对 -> 非零退出。
用法: python -X utf8 produce_two_one.py <uuidA> <uuidB> <name> [fastener]
"""
import sys, os, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import cadquery as cq
from types import SimpleNamespace
import pyarrow.parquet as pq
import assemble_two as a2

import dataset_source
OUTDIR = os.path.join(HERE, "two_part_assemblies")
SRCCACHE = os.path.join(HERE, "_srccache")   # 预建 uuid->源码 缓存(见 build_src_cache.py)


def _load(uuids):
    """取多个 uuid 的源码。返回 {uuid: code}。
    快路径: 若 _srccache/<uuid>.py 存在直接读(O(1), 免扫 parquet)——消除多 worker
    并发线性扫同一批 parquet 造成的磁盘 I/O 争抢(实测把每对 ~29s 拖成瓶颈)。
    缓存缺失的 uuid 才回退扫 parquet, 行为与原来一致。"""
    want = list(dict.fromkeys(uuids))
    found = {}
    for u in want:
        p = os.path.join(SRCCACHE, u + ".py")
        if os.path.isfile(p):
            try:
                found[u] = open(p, encoding="utf-8").read()
            except Exception:
                pass
    missing = set(u for u in want if u not in found)
    if not missing:
        return found
    for f in dataset_source.parquet_files():
        if not missing:
            break
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            for row in pf.read_row_group(
                    rg, columns=["uuid", "cadquery_file"]).to_pylist():
                if row["uuid"] in missing:
                    found[row["uuid"]] = row["cadquery_file"]
                    missing.discard(row["uuid"])
            if not missing:
                break
    return found


def main():
    uA, uB, name = sys.argv[1], sys.argv[2], sys.argv[3]
    fastener = sys.argv[4] if len(sys.argv) > 4 else "socket"
    codes = _load([uA, uB])
    if uA not in codes or uB not in codes:
        print("NOSRC"); sys.exit(2)
    shapeA, srcA = a2.exec_part(codes[uA])
    shapeB, srcB = a2.exec_part(codes[uB])
    if shapeA is None or shapeB is None:
        print("NOSHAPE"); sys.exit(3)

    # 先做一次装配 + 干涉/几何校验, 不通过直接失败(不产出半成品)
    res = a2.assemble_two(shapeA, shapeB, fastener)
    if res is None:
        print("NOPAIR"); sys.exit(4)
    comp, info, anchorsA, anchorsB, recipe, B_moved, align = res
    ok, msgs = a2.verify_geometry(shapeA, B_moved, align, info)
    if not ok:
        for m in msgs:
            print("  " + m)
        print("VERIFY_FAIL"); sys.exit(5)

    # 出 PNG + SVG + DXF(与单件装配一致), STEP + assembly.json + 装配脚本照常。
    out = a2.produce_two(shapeA, shapeB, name, OUTDIR, fastener, srcA, srcB,
                         fmts=("png", "svg", "dxf"))
    if out is None or not out.get("verify_pass"):
        print("NORES"); sys.exit(6)
    print("OK")


if __name__ == "__main__":
    main()
