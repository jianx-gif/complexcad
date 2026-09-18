"""单件装配 worker: 被 batch_assemble 以子进程 + 超时方式调用, 这样一个病态
零件(几何极复杂导致投影/出图卡死)不会拖死整个批量 —— 子进程超时被杀, 主批量
跳过继续。用法: python _produce_one.py <uuid> <name> <fastener>
从 test parquet 按 uuid 取源码、装配、出图。成功打印 'OK', 否则非零退出。
"""
import sys, os, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import cadquery as cq
from types import SimpleNamespace
import pyarrow.parquet as pq
import assemble_fasteners as af

import dataset_source
OUTDIR = os.path.join(HERE, "assemblies")


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
    uuid, name, fastener = sys.argv[1], sys.argv[2], sys.argv[3]
    code = None
    for f in dataset_source.parquet_files():
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            for row in pf.read_row_group(rg, columns=["uuid", "cadquery_file"]).to_pylist():
                if row["uuid"] == uuid:
                    code = row["cadquery_file"]
                    break
            if code is not None:
                break
        if code is not None:
            break
    if code is None:
        print("NOSRC"); sys.exit(2)
    shape, code = exec_part(code)
    if shape is None:
        print("NOSHAPE"); sys.exit(3)
    res = af.produce(shape, name, OUTDIR, fastener=fastener,
                     add_washer=True, add_nut=True, part_source=code)
    if res is None:
        print("NORES"); sys.exit(4)
    print("OK")


if __name__ == "__main__":
    main()
