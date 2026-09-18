"""把已生成的装配脚本(assembly_cadquery.py)精简为 import 零件形式。

原脚本内联了零件完整源码(双件重复2份/单件1份), 占大量篇幅。新生成器改为
exec 子目录 part/(单件) 或 partA,partB/(双件) 的 cadquery.py 取零件几何。
本工具: 遍历装配目录, 从旧脚本解析变换矩阵+紧固件 recipe, 调新生成器重写脚本。
只改 assembly_cadquery.py, 不动几何/step/图纸(确定性不变)。

用法: python -X utf8 slim_assembly_scripts.py [--two] [--single] [--limit N] [--check]
  --check: 只验证前几个精简脚本几何一致, 不批量写。
"""
import os, sys, re, glob, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import cadquery as cq
import assemble_fasteners as af
import assemble_two as a2

TWO = os.path.join(HERE, "two_part_assemblies")
SINGLE = os.path.join(HERE, "assemblies")
KMAP = {"screw": "make_screw", "nut": "make_nut", "washer": "make_washer",
        "bearing": "make_bearing", "heatset": "make_heatset"}
PLACE_RE = re.compile(
    r'fastener\("(\w+)",\s*([^)]*)\).*?axis=\(([^)]+)\),\s*point=\(([^)]+)\),'
    r'\s*seat=([-\d.]+),\s*flip=(\w+)')


def parse_recipe(old):
    recipe = []
    for pm in PLACE_RE.finditer(old):
        kind, args, ax, pt, seat, flip = pm.groups()
        arglist = []
        for a in args.split(","):
            a = a.strip().strip("'\"")
            if a == "":
                continue
            try:
                arglist.append(int(a) if a.lstrip("-").isdigit() else float(a))
            except ValueError:
                arglist.append(a)
        recipe.append({"factory": KMAP.get(kind, "make_" + kind), "args": arglist,
                       "a": [float(x) for x in ax.split(",")],
                       "p": [float(x) for x in pt.split(",")],
                       "t": float(seat), "flip": flip == "True"})
    return recipe


def slim_two(d):
    old_f = os.path.join(d, "assembly_cadquery.py")
    if not os.path.isfile(old_f):
        return None
    old = open(old_f, encoding="utf-8").read()
    mrow = re.search(r"_t\.SetValues\(([^)]+)\)", old)
    if not mrow:
        return None
    m = [float(x) for x in mrow.group(1).split(",")]
    recipe = parse_recipe(old)
    srcA = open(os.path.join(d, "partA", "cadquery.py"), encoding="utf-8").read()
    srcB = open(os.path.join(d, "partB", "cadquery.py"), encoding="utf-8").read()
    return a2._finalize_script(af._asm_header(os.path.abspath(d)), srcA, srcB, m,
                               recipe, here_abs=os.path.abspath(d))


def slim_single(d):
    old_f = os.path.join(d, "assembly_cadquery.py")
    pf = os.path.join(d, "part", "cadquery.py")
    if not (os.path.isfile(old_f) and os.path.isfile(pf)):
        return None
    old = open(old_f, encoding="utf-8").read()
    recipe = parse_recipe(old)
    if not recipe:
        return None
    body = open(pf, encoding="utf-8").read()
    return af.build_assembly_script(body, recipe, here_abs=os.path.abspath(d))


def geom_ok(d, slim):
    """执行精简脚本, 与旧脚本比 bbox+体积。返回 (ok, msg)。"""
    tmp = os.path.join(d, "_slim_chk.py")
    try:
        open(tmp, "w", encoding="utf-8").write(slim)
        g = {"__file__": tmp, "__name__": "x"}
        exec(compile(slim, tmp, "exec"), g)
        s = g["result"]; s = s.val() if hasattr(s, "val") else s
        b = s.BoundingBox()
        old = open(os.path.join(d, "assembly_cadquery.py"), encoding="utf-8").read()
        g2 = {"__file__": os.path.join(d, "assembly_cadquery.py"), "__name__": "x"}
        exec(compile(old, "old", "exec"), g2)
        s2 = g2["result"]; s2 = s2.val() if hasattr(s2, "val") else s2
        b2 = s2.BoundingBox()
        derr = max(abs(b.xlen-b2.xlen), abs(b.ylen-b2.ylen), abs(b.zlen-b2.zlen))
        verr = abs(s.Volume() - s2.Volume())
        return (derr < 1e-6 and verr < 1e-3), "bbox_err=%.1e vol_err=%.1e" % (derr, verr)
    except Exception as e:
        return False, "%s: %s" % (type(e).__name__, str(e)[:60])
    finally:
        if os.path.isfile(tmp):
            os.remove(tmp)


def run(root, slim_fn, glob_pat, args):
    dirs = sorted(glob.glob(os.path.join(root, glob_pat)))
    if args.limit:
        dirs = dirs[:args.limit]
    n_ok = n_fail = n_skip = 0
    lens_old = lens_new = 0
    for d in dirs:
        slim = slim_fn(d)
        if slim is None:
            n_skip += 1
            continue
        if args.check:
            ok, msg = geom_ok(d, slim)
            print("  [%s] %s  %s" % ("OK" if ok else "FAIL", os.path.basename(d)[:30], msg))
            if ok: n_ok += 1
            else: n_fail += 1
            continue
        old_f = os.path.join(d, "assembly_cadquery.py")
        lens_old += len(open(old_f, encoding="utf-8").read().splitlines())
        lens_new += len(slim.splitlines())
        open(old_f, "w", encoding="utf-8").write(slim)
        n_ok += 1
        if n_ok % 200 == 0:
            print("  写入 %d ..." % n_ok, flush=True)
    tag = os.path.basename(root)
    if args.check:
        print("%s 验证: OK %d, FAIL %d, 跳过 %d" % (tag, n_ok, n_fail, n_skip))
    else:
        print("%s 精简: 重写 %d 个, 跳过 %d; 总行数 %d -> %d (省 %.0f%%)"
              % (tag, n_ok, n_skip, lens_old, lens_new,
                 100 * (1 - lens_new / max(lens_old, 1))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--two", action="store_true")
    ap.add_argument("--single", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.two or args.single):
        args.two = args.single = True
    if args.two:
        run(TWO, slim_two, "*__two", args)
    if args.single:
        run(SINGLE, slim_single, "*__asm", args)


if __name__ == "__main__":
    main()
