"""双版本装配脚本产出(不破坏原版数据):
  - 原目录 assemblies/ two_part_assemblies/ 的 assembly_cadquery.py -> **原版内联长脚本**
    (自包含, 内嵌零件源码, 无外部依赖)
  - 新平行目录 assemblies_slim/ two_part_assemblies_slim/ -> **精简版**
    (只放 assembly_cadquery.py, 引用原目录 partA/partB/part 的零件; 硬编码路径, CQ-editor 可跑)

从当前盘上的 assembly_cadquery.py 解析变换矩阵 m + 紧固件 recipe(精简/内联版都含
SetValues+place, 可解析), 零件源码从 partA/partB/part/cadquery.py 读。
只写脚本文件, 不动几何/step/图/零件。

用法: python -X utf8 build_assembly_variants.py [--two] [--single] [--limit N]
"""
import os, sys, re, glob, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import assemble_fasteners as af
import assemble_two as a2

TWO = os.path.join(HERE, "two_part_assemblies")
SINGLE = os.path.join(HERE, "assemblies")
TWO_SLIM = os.path.join(HERE, "two_part_assemblies_slim")
SINGLE_SLIM = os.path.join(HERE, "assemblies_slim")
KMAP = {"screw": "make_screw", "nut": "make_nut", "washer": "make_washer",
        "bearing": "make_bearing", "heatset": "make_heatset"}
PLACE_RE = re.compile(
    r'fastener\("(\w+)",\s*([^)]*)\).*?axis=\(([^)]+)\),\s*point=\(([^)]+)\),'
    r'\s*seat=([-\d.]+),\s*flip=(\w+)')


def parse_recipe(txt):
    recipe = []
    for pm in PLACE_RE.finditer(txt):
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


def run_two(limit):
    dirs = sorted(glob.glob(os.path.join(TWO, "*__two")))
    if limit:
        dirs = dirs[:limit]
    os.makedirs(TWO_SLIM, exist_ok=True)
    n = 0
    for d in dirs:
        f = os.path.join(d, "assembly_cadquery.py")
        pa = os.path.join(d, "partA", "cadquery.py")
        pb = os.path.join(d, "partB", "cadquery.py")
        if not (os.path.isfile(f) and os.path.isfile(pa) and os.path.isfile(pb)):
            continue
        txt = open(f, encoding="utf-8").read()
        mrow = re.search(r"_t\.SetValues\(([^)]+)\)", txt)
        if not mrow:
            continue
        m = [float(x) for x in mrow.group(1).split(",")]
        recipe = parse_recipe(txt)
        srcA = open(pa, encoding="utf-8").read()
        srcB = open(pb, encoding="utf-8").read()
        name = os.path.basename(d)
        # ① 原目录: 内联长脚本(自包含)
        inline = a2._finalize_script_inline(af._ASM_HEADER.rstrip("\n"), srcA, srcB, m, recipe)
        open(f, "w", encoding="utf-8").write(inline)
        # ② 新 _slim 目录: 精简版, **自包含相对路径**。复制 partA/partB 的 cadquery.py
        #    进 slim 目录, 脚本用相对路径(_HERE=脚本自身目录)加载, 不再硬编码绝对路径。
        sd = os.path.join(TWO_SLIM, name)
        os.makedirs(os.path.join(sd, "partA"), exist_ok=True)
        os.makedirs(os.path.join(sd, "partB"), exist_ok=True)
        open(os.path.join(sd, "partA", "cadquery.py"), "w", encoding="utf-8").write(srcA)
        open(os.path.join(sd, "partB", "cadquery.py"), "w", encoding="utf-8").write(srcB)
        # 相对 header(_ASM_HEADER): _HERE = 脚本目录, sys.path 加上一级(slim 根)找
        # 共享 fasteners.py/library_parts.py; _load_part 从 _HERE/partX 读零件。
        slim = a2._finalize_script(af._ASM_HEADER.rstrip("\n"), srcA, srcB, m, recipe)
        open(os.path.join(sd, "assembly_cadquery.py"), "w", encoding="utf-8").write(slim)
        n += 1
        if n % 200 == 0:
            print("  双件 %d ..." % n, flush=True)
    print("双件: 原目录恢复内联版 + %s/ 精简版, 共 %d 件" % (os.path.basename(TWO_SLIM), n))


def run_single(limit):
    dirs = sorted(glob.glob(os.path.join(SINGLE, "*__asm")))
    if limit:
        dirs = dirs[:limit]
    os.makedirs(SINGLE_SLIM, exist_ok=True)
    n = 0
    for d in dirs:
        f = os.path.join(d, "assembly_cadquery.py")
        pf = os.path.join(d, "part", "cadquery.py")
        if not (os.path.isfile(f) and os.path.isfile(pf)):
            continue
        txt = open(f, encoding="utf-8").read()
        recipe = parse_recipe(txt)
        if not recipe:
            continue
        body = open(pf, encoding="utf-8").read()
        name = os.path.basename(d)
        # ① 原目录: 内联长脚本
        inline = af.build_assembly_script_inline(body, recipe)
        open(f, "w", encoding="utf-8").write(inline)
        # ② 新 _slim 目录: 精简版, **自包含相对路径**。复制 part/ 的 cadquery.py 进
        #    slim 目录, 脚本用相对路径(_HERE=脚本自身目录), 不硬编码绝对路径。
        sd = os.path.join(SINGLE_SLIM, name)
        os.makedirs(os.path.join(sd, "part"), exist_ok=True)
        open(os.path.join(sd, "part", "cadquery.py"), "w", encoding="utf-8").write(body)
        slim = af.build_assembly_script(body, recipe)   # here_abs=None -> 相对 header
        open(os.path.join(sd, "assembly_cadquery.py"), "w", encoding="utf-8").write(slim)
        n += 1
        if n % 200 == 0:
            print("  单件 %d ..." % n, flush=True)
    print("单件: 原目录恢复内联版 + %s/ 精简版, 共 %d 件" % (os.path.basename(SINGLE_SLIM), n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--two", action="store_true")
    ap.add_argument("--single", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    if not (args.two or args.single):
        args.two = args.single = True
    if args.two:
        run_two(args.limit)
    if args.single:
        run_single(args.limit)


if __name__ == "__main__":
    main()
