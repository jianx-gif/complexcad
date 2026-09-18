import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
width = 15.0
split_gap_width = 2.0
slot_width = 4.0
slot_depth = 10.0
slot_count = 8
chamfer_dist = 0.5

base = (
    cq.Workplane('XY')
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(width)
)

split_cut = (
    cq.Workplane('XY')
    .center(outer_diameter / 2 - split_gap_width / 2, 0)
    .rect(split_gap_width, outer_diameter)
    .extrude(width + 2.0)
)

slot_cut = (
    cq.Workplane('XY')
    .center(0, outer_diameter / 2 - slot_depth / 2)
    .rect(slot_width, slot_depth)
    .extrude(width + 2.0)
)

result = base.cut(split_cut)

angle_step = 360.0 / slot_count
for i in range(slot_count):
    result = result.cut(slot_cut.rotate((0, 0, 0), (0, 0, 1), i * angle_step))

result = result.edges().chamfer(chamfer_dist)
