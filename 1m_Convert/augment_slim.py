"""给两种 slim 目录的每个装配补齐其它模态。

- two_part_assemblies_slim/<a8>_<b8>__M?__two/: 读它自己的 partA/partB 源码,
  调 assemble_two.produce_two(keep_script=True) 在该目录生成
  model.step/stl + drawing.{png,svg,dxf} + assembly.json。
- assemblies_slim/<uuid>__M?_socket__asm/: 读它自己的 part/ 源码,
  调 assemble_fasteners.produce(keep_script=True) 同样补齐模态。

keep_script=True: 不覆盖目录里已有的相对路径装配脚本, 只补模态。
结果由 slim 目录各自的零件源码真实生成, 与非 slim 目录一致。

用法: python -X utf8 augment_slim.py [--kind two|single|both] [--jobs N]
                                     [--limit N] [--names-file f]
"""
import sys, os, glob, argparse, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

TWO_SLIM = os.path.join(HERE, "two_part_assemblies_slim")
SINGLE_SLIM = os.path.join(HERE, "assemblies_slim")


def _read(p):
    return open(p, encoding="utf-8").read()


def _one_two(name):
    """双件: 补全一个 slim 目录。"""
    import assemble_two as a2
    d = os.path.join(TWO_SLIM, name)
    pa = os.path.join(d, "partA", "cadquery.py")
    pb = os.path.join(d, "partB", "cadquery.py")
    if not (os.path.isfile(pa) and os.path.isfile(pb)):
        return (name, False, "no partA/partB")
    try:
        shapeA, srcA = a2.exec_part(_read(pa))
        shapeB, srcB = a2.exec_part(_read(pb))
        if shapeA is None or shapeB is None:
            return (name, False, "exec part -> None")
        out = a2.produce_two(shapeA, shapeB, name, TWO_SLIM, "socket",
                             srcA=srcA, srcB=srcB, fmts=("png", "svg", "dxf"),
                             skip_verify=True, keep_script=True)
        if out is None:
            return (name, False, "produce_two None")
        return (name, True, "")
    except Exception as e:
        return (name, False, type(e).__name__ + ": " + str(e)[:80])


def _one_single(name):
    """单件: 补全一个 slim 目录。"""
    import assemble_two as a2
    import assemble_fasteners as af
    d = os.path.join(SINGLE_SLIM, name)
    pf = os.path.join(d, "part", "cadquery.py")
    if not os.path.isfile(pf):
        return (name, False, "no part/")
    try:
        src = _read(pf)
        shape, src2 = a2.exec_part(src)
        if shape is None:
            return (name, False, "exec part -> None")
        # Z2C_RERENDER=1: 目录已有带螺纹 model.step/stl(如已生成过的 slim), 只需
        # 重出图(如应用 ISO 中心线修复)——走 rerender_only 跳过带螺纹重建模(4.8s/件)
        # 与 3D 重导出, 提速数倍; 脚本受 rerender_only+keep_script 双重保护不被改写。
        ro = os.environ.get("Z2C_RERENDER") == "1"
        # rerender 模式只为把**装配图**应用 ISO 中心线修复(build_revolution_axes)。
        # 零件图走 make_drawings(未改动), 重画产出完全相同 -> 跳过它(want_part_drawing
        # =False)省掉 md.process(姿态归一+参数提取+ISO标注)这一大头, 无任何质量损失。
        out = af.produce(shape, name, SINGLE_SLIM, fastener="socket",
                         part_source=src2, keep_script=True, rerender_only=ro,
                         want_part_drawing=(not ro))
        if out is None:
            return (name, False, "produce None")
        return (name, True, "")
    except Exception as e:
        return (name, False, type(e).__name__ + ": " + str(e)[:80])


def _run(names, worker, jobs, label):
    t0 = time.time()
    ok = fail = 0
    print(f"[{label}] 共 {len(names)} 个, jobs={jobs}", flush=True)
    with Pool(jobs) as pool:
        for i, (name, good, err) in enumerate(pool.imap_unordered(worker, names), 1):
            if good:
                ok += 1
            else:
                fail += 1
                print(f"  FAIL {name}: {err}", flush=True)
            if i % 50 == 0:
                el = time.time() - t0
                print(f"  [{label}] 进度 {i}/{len(names)} ok{ok} fail{fail} "
                      f"{i/el:.2f}件/s ETA {(len(names)-i)/(i/el)/60:.1f}min",
                      flush=True)
    print(f"[{label}] 完成: ok {ok}, fail {fail} / {len(names)} "
          f"用时 {(time.time()-t0)/60:.1f}min", flush=True)
    return ok, fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=("two", "single", "both"), default="both")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--names-file", default=None)
    ap.add_argument("--rerender", action="store_true",
                    help="仅重出图(目录已有 3D 模型时): 跳过带螺纹重建模+3D重导出, "
                         "只重画工程图(如应用 ISO 中心线修复), 快数倍。经环境变量传子进程。")
    args = ap.parse_args()
    if args.rerender:
        os.environ["Z2C_RERENDER"] = "1"      # spawn 子进程继承此环境变量

    want = None
    if args.names_file:
        want = set(l.strip() for l in open(args.names_file, encoding="utf-8")
                   if l.strip())

    if args.kind in ("two", "both"):
        names = [os.path.basename(x)
                 for x in sorted(glob.glob(os.path.join(TWO_SLIM, "*__two")))]
        if want:
            names = [n for n in names if n in want]
        if args.limit:
            names = names[:args.limit]
        _run(names, _one_two, args.jobs, "双件slim")

    if args.kind in ("single", "both"):
        names = [os.path.basename(x)
                 for x in sorted(glob.glob(os.path.join(SINGLE_SLIM, "*__asm")))]
        if want:
            names = [n for n in names if n in want]
        if args.limit:
            names = names[:args.limit]
        _run(names, _one_single, args.jobs, "单件slim")


if __name__ == "__main__":
    main()
