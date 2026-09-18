"""CadQuery -> STEP 精度往返核查 (自包含, 可独立运行)。

核查: cadquery.py 里的(含小数)参数 -> 导出的 model.step 文件实际几何尺寸 误差有多少。
方法: 对 cases/ 下每个件, (1)执行 cadquery.py 得源码几何并量 bounding box,
(2)载入同目录 model.step 重新量 bbox, (3)对比两者差(STEP 往返是否无损);
(4)grep STEP 文件内坐标, 看保留多少位有效数字。

用法: python -X utf8 step_roundtrip_test.py
依赖: cadquery (与生成数据集同环境)。cases/ 内是从 output/ 复制的 3 个带小数参数的样例。
"""
import sys, os, glob, re, math
import cadquery as cq
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cases")

cases = [
    "0310bb67-a4fe-f541-1ecc-69f03df49e87",  # boss_fillet=0.75
    "0a4c4de1-6ed5-b516-25a8-1bb9a9bc5a28",  # scale_factor=0.85 -> 派生尺寸 78.249641
    "071a220d-5b4e-fc1d-c9ce-3a3a3b23b0ab",  # tolerance=0.01 -> 派生尺寸 98.994949
]


def exec_part(src):
    g = {"cq": cq, "SimpleNamespace": SimpleNamespace, "math": math, "__name__": "x"}
    exec(src, g)
    r = g.get("result")
    if r is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                r = v
    return r


for uuid in cases:
    d = os.path.join(OUT, uuid)
    src = open(os.path.join(d, "cadquery.py"), encoding="utf-8", errors="ignore").read()
    print("=" * 60)
    print(uuid)
    # 源码几何 bbox
    try:
        shp = exec_part(src)
        s = shp.val() if hasattr(shp, "val") else shp
        bb = s.BoundingBox()
        src_dims = (bb.xlen, bb.ylen, bb.zlen)
        print("  源码执行几何 bbox: [%.6f, %.6f, %.6f]" % src_dims)
    except Exception as e:
        print("  源码执行失败:", type(e).__name__, str(e)[:60]); continue
    # STEP 载入几何 bbox
    try:
        step_shp = cq.importers.importStep(os.path.join(d, "model.step"))
        ss = step_shp.val() if hasattr(step_shp, "val") else step_shp
        sbb = ss.BoundingBox()
        step_dims = (sbb.xlen, sbb.ylen, sbb.zlen)
        print("  STEP 载入几何 bbox: [%.6f, %.6f, %.6f]" % step_dims)
        # 误差
        errs = [abs(a - b) for a, b in zip(src_dims, step_dims)]
        print("  bbox 往返误差(mm): [%.2e, %.2e, %.2e]  最大 %.2e" % (errs[0], errs[1], errs[2], max(errs)))
    except Exception as e:
        print("  STEP 载入失败:", type(e).__name__, str(e)[:60])
    # STEP 文件里坐标的有效位数(看精度保留)
    txt = open(os.path.join(d, "model.step"), encoding="utf-8", errors="ignore").read()
    coords = re.findall(r"-?\d+\.\d+E?-?\d*", txt)
    # 找带最多小数位的坐标样例
    longest = sorted(set(coords), key=lambda x: -len(x))[:6]
    print("  STEP 文件内坐标精度样例(最长数字):", longest)
    print()
