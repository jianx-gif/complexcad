import cadquery as cq

# 精度测试: 盒子边长直接 = outer_side 本身(无派生运算)。
# STEP 模型里量出的边长应精确等于 outer_side。
outer_side = 70.123
height = 10.0

result = cq.Workplane("XY").box(outer_side, outer_side, height)
