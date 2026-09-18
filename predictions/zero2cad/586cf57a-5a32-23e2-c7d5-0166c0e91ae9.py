import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
thickness = 15.0
slot_width = 4.0
slot_depth = 10.0
num_slots = 8
chamfer_size = 0.5

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

slot = (
    cq.Workplane("XY")
    .center(outer_radius - slot_depth / 2.0, 0)
    .rect(slot_depth, slot_width)
    .extrude(thickness)
)

result = base
for i in range(num_slots):
    angle = i * 360.0 / num_slots
    result = result.cut(slot.rotate((0, 0, 0), (0, 0, 1), angle))

result = result.edges().chamfer(chamfer_size)
