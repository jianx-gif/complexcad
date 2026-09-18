"""对【转换后(量化整数坐标)】的 py 脚本走完整管线:
   量化 cadquery.py -> model.step + model.stl -> 工程图(png/svg/dxf)

与 output_koor 用原始代码不同, 这里用 converted_py/<uuid>/cadquery.py (量化代码),
产出的几何坐标在 [1,10000] 盒子里, 工程图尺寸是放大值(如 7000 而非 70mm)。
输出到独立目录 koor_geometry/<uuid>/, 不碰外面已完成的 output/。

用法: python build_koor_geometry.py <uuid> [<uuid> ...]
      python build_koor_geometry.py --all [N]
"""
import sys, os, glob, shutil, json, traceback, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)          # 1m_Convert/ (脚本移入 koor/ 后, 数据目录在上一级)
ROOT = os.path.dirname(PARENT)          # 项目根 (含 match/make_drawings 等核心脚本)
if importlib.util.find_spec("match") is None:   # not pip-installed (complexcad-koor): run from the checkout
    sys.path.insert(0, ROOT)

import cadquery as cq
from types import SimpleNamespace
import math
import match   # to raise the integer-snap tolerance for quantized geometry

SRC = os.path.join(PARENT, "converted_py")         # 量化代码来源
OUT = os.path.join(PARENT, "koor_geometry")        # 隔离输出


def exec_to_shape(code):
    g = {"cq": cq, "SimpleNamespace": SimpleNamespace, "math": math,
         "__name__": "__cqexec__"}
    exec(code, g)
    r = g.get("result")
    if r is None:
        for v in g.values():
            if isinstance(v, cq.Workplane):
                r = v
    if r is None:
        raise RuntimeError("no result")
    return r


def build_one(uuid):
    src = os.path.join(SRC, uuid, "cadquery.py")
    if not os.path.isfile(src):
        raise FileNotFoundError(src)
    code = open(src, encoding="utf-8").read()
    d = os.path.join(OUT, uuid)
    os.makedirs(d, exist_ok=True)
    # 落地量化代码本身, 方便对照
    shutil.copy(src, os.path.join(d, "cadquery.py"))
    kj = os.path.join(SRC, uuid, "koor.json")
    scale = 100.0
    if os.path.isfile(kj):
        shutil.copy(kj, os.path.join(d, "koor.json"))
        try:
            scale = float(json.load(open(kj, encoding="utf-8")).get("scale", 100.0))
        except Exception:
            scale = 100.0
    # 量化几何放大了 ~scale 倍, tessellation 噪声(原 ~0.02mm)也放大成几个整数单位。
    # 1) 容差按 scale 放大, 量化图才不会标 7000.38 这种小数;
    # 2) 吸附网格设为 scale: 量化尺寸吸附到最近的 scale 倍数 = 还原成整毫米设计值
    #    (299.47 -> 300), 否则就近取整会把 299.47 错吸成 299。
    match._SNAP_TOL = 0.12 * scale
    match._SNAP_GRID = scale
    # 非整 scale 的大件: 吸附到网格后的值本身仍是小数(35*89.2=3121.86),
    # 显示时再取整成 3122, 大件工程图才是整数标注。
    match._SNAP_INT_DISPLAY = abs(scale - round(scale)) > 1e-6
    # 1) 执行量化代码 -> STEP + STL
    r = exec_to_shape(code)
    shape = r.val() if hasattr(r, "val") else r
    cq.exporters.export(r, os.path.join(d, "model.step"))
    cq.exporters.export(r, os.path.join(d, "model.stl"))
    # 2) 工程图: 复用现有管线, 把 OUT 重定向到隔离目录
    import make_drawings as md
    md.OUT = OUT
    # 量化测试版: 降低剖视阈值(4.0->2.5, 覆盖约1/3件), 让有内部结构的大件
    # 多触发剖视; 并放宽内部尺寸上限, 加强大件内部标注完整度。
    md.SECTION_RATIO = 2.5
    match._WALL_MAX_NEW = 8
    match._SECTION_MAX = 10
    match._LOC_MAX = 8
    md.process(uuid)
    # 3) 其余三模态: 点云(npy/ply) + BREP + 文本描述, 与正式 output/ 对齐。
    #    augment 读 metadata.json 的 cadquery_ops_json 生成操作序列文本; 量化件
    #    没有 metadata, 先从量化代码解析出 op 序列写个最小 metadata, 文本才完整。
    _write_min_metadata(d, uuid, code)
    import augment_data as aug
    aug.OUT = OUT
    aug.augment(uuid)
    return d


def _write_min_metadata(folder, uuid, code):
    """从量化 cadquery 代码解析建模操作序列, 写最小 metadata.json 供文本描述使用。"""
    import ast
    import json as _json
    ops = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                ops.append({"op_name": node.func.attr, "function": node.func.attr})
    except Exception:
        ops = []
    meta = {"uuid": uuid, "cadquery_ops_json": ops,
            "cadquery_ops_count": len(ops)}
    mp = os.path.join(folder, "metadata.json")
    if not os.path.isfile(mp):
        _json.dump(meta, open(mp, "w", encoding="utf-8"),
                   ensure_ascii=False, indent=2)


def main():
    args = sys.argv[1:]
    os.makedirs(OUT, exist_ok=True)
    if args and args[0] == "--all":
        n = int(args[1]) if len(args) > 1 else 0
        uuids = [os.path.basename(os.path.normpath(p))
                 for p in sorted(glob.glob(os.path.join(SRC, "*", "")))]
        if n:
            uuids = uuids[:n]
    else:
        uuids = args
    ok = fail = 0
    for u in uuids:
        try:
            build_one(u)
            ok += 1
            print(f"  [ok]   {u}", flush=True)
        except Exception as e:
            fail += 1
            print(f"  [FAIL] {u[:8]} {type(e).__name__}: {str(e)[:80]}", flush=True)
    print(f"完成: ok={ok} fail={fail} -> {OUT}\\<uuid>\\", flush=True)


if __name__ == "__main__":
    main()
