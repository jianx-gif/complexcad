"""把每个装配子目录里的通用依赖(fasteners.py / library_parts.py)去重为共享一份:
- 在输出根目录(assemblies/ 和 two_part_assemblies/)各保留一份共享副本。
- 删除每个子目录里的副本。
- 给旧版 assembly_cadquery.py(头部没有 sys.path 行的)补上 sys.path, 使其仍能从
  根目录解析共享依赖、独立重跑。新版脚本(已含 sys.path)不动。
幂等可重复运行。
"""
import os, glob, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)          # 1m_Convert/ (脚本移入 koor/ 后, 装配核心+数据目录在上一级)
DEPS = ("fasteners.py", "library_parts.py")
SYS_PATH_LINE = (
    "import os, sys\n"
    "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n"
)


def fix_root(root):
    if not os.path.isdir(root):
        return 0, 0
    # 1) 确保根目录有共享副本
    for hp in DEPS:
        dst = os.path.join(root, hp)
        if not os.path.isfile(dst):
            shutil.copyfile(os.path.join(PARENT, hp), dst)
    deleted = 0
    fixed = 0
    for d in glob.glob(os.path.join(root, "*")):
        if not os.path.isdir(d):
            continue
        # 2) 脚本头部补 sys.path(旧版没有)
        sp = os.path.join(d, "assembly_cadquery.py")
        if os.path.isfile(sp):
            src = open(sp, encoding="utf-8").read()
            if "sys.path.insert" not in src.split("\n", 6)[0:6].__str__():
                # 更稳: 检查前几行是否已有 sys.path
                head = "\n".join(src.splitlines()[:5])
                if "sys.path.insert" not in head:
                    open(sp, "w", encoding="utf-8").write(SYS_PATH_LINE + src)
                    fixed += 1
        # 3) 删子目录里的依赖副本
        for hp in DEPS:
            f = os.path.join(d, hp)
            if os.path.isfile(f):
                os.remove(f)
                deleted += 1
        # 顺手清 __pycache__
        pc = os.path.join(d, "__pycache__")
        if os.path.isdir(pc):
            shutil.rmtree(pc, ignore_errors=True)
    return deleted, fixed


def main():
    total_del = total_fix = 0
    for root in ("assemblies", "two_part_assemblies"):
        rp = os.path.join(PARENT, root)
        d, f = fix_root(rp)
        total_del += d; total_fix += f
        print("%s: 删除副本 %d, 补脚本头 %d" % (root, d, f))
    print("合计: 删除 %d 个冗余依赖副本, 修正 %d 个脚本头" % (total_del, total_fix))


if __name__ == "__main__":
    main()
