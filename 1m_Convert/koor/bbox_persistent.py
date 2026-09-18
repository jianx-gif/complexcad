"""常驻 bbox worker: import cadquery 一次, 逐行读 {code} 执行, 返回 {bb:[xl,yl,zl,xmin,ymin,zmin]}。"""
import sys, os, json
# 管道用 UTF-8 并重设行缓冲: Windows 下默认 stdout 编码会在写管道时报 Errno 22。
try:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    sys.stdin.reconfigure(encoding="utf-8", newline="\n")
except Exception:
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery as cq
from types import SimpleNamespace
import math


def run(src):
    g = {"cq": cq, "SimpleNamespace": SimpleNamespace, "math": math, "__name__": "__cqexec__"}
    exec(src, g)
    res = g.get("result")
    if res is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                res = v
    if res is None:
        raise RuntimeError("no result")
    shape = res.val() if hasattr(res, "val") else res
    bb = shape.BoundingBox()
    return [bb.xlen, bb.ylen, bb.zlen, bb.xmin, bb.ymin, bb.zmin]


def main():
    sys.stdout.write("READY\n"); sys.stdout.flush()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            out = {"bb": run(json.loads(line)["code"])}
        except Exception as e:
            out = {"error": f"{type(e).__name__}: {e}"}
        sys.stdout.write(json.dumps(out) + "\n"); sys.stdout.flush()


if __name__ == "__main__":
    main()
