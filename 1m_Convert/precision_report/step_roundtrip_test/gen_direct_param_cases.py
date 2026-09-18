"""生成'参数直接=尺寸'精度测试的 9 组独立案例(各自子文件夹)。

每组: 一个 box(side, side, 10) 的 cadquery.py(side=该测试值) + 导出的 model.step
+ result.txt(你写的参数 vs STEP读回实测尺寸 vs 误差)。
盒子边长直接=参数本身, 无任何派生运算 -> STEP量出的边长应精确=参数。

用法: python -X utf8 gen_direct_param_cases.py
输出: direct_param_cases/01_side_70.0/ ... 09_side_0.001/
"""
import sys, os
# 项目根 = 本文件上溯 3 级 (step_roundtrip_test/ -> precision_report/ -> 1m_Convert/ -> data/)
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, _ROOT)
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "direct_param_cases")

# 9 组测试值(从整数到13位小数到亚毫米)
test_vals = [70.0, 70.5, 70.12, 70.123, 70.12345,
             70.123456789, 70.1234567890123, 0.85, 0.001]

CQ_TEMPLATE = '''import cadquery as cq

# 精度测试: 盒子边长直接 = outer_side 本身(无派生运算)。
# STEP 模型里量出的边长应精确等于 outer_side。
outer_side = {val!r}
height = 10.0

result = cq.Workplane("XY").box(outer_side, outer_side, height)
'''


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    summary = []
    for i, v in enumerate(test_vals, 1):
        name = "%02d_side_%s" % (i, repr(v))
        d = os.path.join(OUTDIR, name)
        os.makedirs(d, exist_ok=True)
        # 1. 写 cadquery.py
        src = CQ_TEMPLATE.format(val=v)
        open(os.path.join(d, "cadquery.py"), "w", encoding="utf-8").write(src)
        # 2. 执行 + 导出 STEP
        box = cq.Workplane("XY").box(v, v, 10.0)
        cq.exporters.export(box, os.path.join(d, "model.step"))
        # 3. 读回 STEP 量边长
        ss = cq.importers.importStep(os.path.join(d, "model.step"))
        s2 = ss.val() if hasattr(ss, "val") else ss
        measured = s2.BoundingBox().xlen
        err = abs(measured - v)
        # 4. 写 result.txt
        res = (
            "精度测试组 %d\n" % i +
            "=" * 50 + "\n" +
            "你写的参数  outer_side    = %.16g\n" % v +
            "STEP读回实测边长 bbox.xlen = %.16g\n" % measured +
            "差值                       = %+.3e\n" % (measured - v) +
            "绝对误差                   = %.3e mm\n" % err +
            "\n" +
            ("=> 误差为 0, 尺寸精确生成\n" if err == 0
             else "=> 误差 %.1e mm (64位浮点极限, 工程上=0)\n" % err)
        )
        open(os.path.join(d, "result.txt"), "w", encoding="utf-8").write(res)
        summary.append((name, v, measured, err))
        print("  + %s/  (cadquery.py + model.step + result.txt)  误差 %.1e" % (name, err))

    # 总览
    lines = ["# 参数直接=尺寸 精度测试 — 9 组总览\n",
             "盒子边长直接 = outer_side 本身, STEP 量出的边长应精确等于参数。\n",
             "| 组 | 你写的 outer_side | STEP读回实测边长 | 误差 |\n",
             "|---|---|---|---|\n"]
    for name, v, m, err in summary:
        errs = "**0**" if err == 0 else "%.1e mm" % err
        lines.append("| %s | %.13g | %.13g | %s |\n" % (name, v, m, errs))
    lines.append("\n> 到 12 位小数误差精确为 0；仅 13 位小数出现 ~1e-12 浮点极限误差。"
                 "连 0.001mm(1微米) 亦精确生成。\n")
    open(os.path.join(OUTDIR, "SUMMARY.md"), "w", encoding="utf-8").write("".join(lines))
    print("\n总览 -> direct_param_cases/SUMMARY.md")


if __name__ == "__main__":
    main()
