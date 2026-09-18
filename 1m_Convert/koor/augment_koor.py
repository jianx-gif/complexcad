"""给已生成的量化件 (koor_geometry/<uuid>/) 批量补齐三模态:
点云(npy/ply) + BREP + 文本描述。已有 point_cloud.npy 的跳过(可续传)。
用法: python augment_koor.py [N]
"""
import sys, os, glob, ast, json, traceback, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)          # 1m_Convert/ (脚本移入 koor/ 后, 数据目录在上一级)
ROOT = os.path.dirname(PARENT)          # 项目根 (含 augment_data 等核心脚本)
if importlib.util.find_spec("augment_data") is None:   # not pip-installed (complexcad-koor): run from the checkout
    sys.path.insert(0, ROOT)
import augment_data as aug

OUT = os.path.join(PARENT, "koor_geometry")
aug.OUT = OUT


def write_min_metadata(folder, uuid):
    mp = os.path.join(folder, "metadata.json")
    if os.path.isfile(mp):
        return
    ops = []
    try:
        tree = ast.parse(open(os.path.join(folder, "cadquery.py"),
                              encoding="utf-8").read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                ops.append({"op_name": node.func.attr, "function": node.func.attr})
    except Exception:
        ops = []
    json.dump({"uuid": uuid, "cadquery_ops_json": ops,
               "cadquery_ops_count": len(ops)},
              open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    dirs = sorted(glob.glob(os.path.join(OUT, "*", "")))
    if n:
        dirs = dirs[:n]
    ok = skip = fail = 0
    for d in dirs:
        u = os.path.basename(os.path.normpath(d))
        if os.path.isfile(os.path.join(d, "point_cloud.npy")):
            skip += 1
            continue
        if not os.path.isfile(os.path.join(d, "model.step")) \
                or not os.path.isfile(os.path.join(d, "model.stl")):
            fail += 1
            print(f"  [FAIL] {u[:8]} 缺 step/stl", flush=True)
            continue
        try:
            write_min_metadata(d, u)
            aug.augment(u)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"  [FAIL] {u[:8]} {type(e).__name__}: {str(e)[:70]}", flush=True)
    print(f"完成: 补齐 {ok}  跳过(已有) {skip}  失败 {fail}", flush=True)


if __name__ == "__main__":
    main()
