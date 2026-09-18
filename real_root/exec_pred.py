"""执行一个预测的 CadQuery 代码并导出 STL: python exec_pred.py <pred.py> <out.stl>
取 result 变量或最后一个 cq.Workplane。exit 0=成功。"""
import sys
import cadquery as cq

src, out = sys.argv[1], sys.argv[2]
code = open(src, encoding="utf-8").read()
ns = {}
exec(code, {"cq": cq, "cadquery": cq}, ns)
solid = ns.get("result") or ns.get("r")
if solid is None:
    for v in reversed(list(ns.values())):
        if isinstance(v, cq.Workplane):
            solid = v
            break
assert solid is not None, "no Workplane result"
cq.exporters.export(solid, out)
print("OK", out)
