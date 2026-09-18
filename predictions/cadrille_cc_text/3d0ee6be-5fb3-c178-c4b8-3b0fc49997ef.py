import cadquery as cq
base_radius = 20.0
top_radius = 30.0
height = 50.0
chamfer_distance = 1.0
mount_hole_diameter = 5.0
mount_hole_count = 4
slot_width = 10.0
slot_depth = 5.0
slot_count = 6
fillet_radius = 2.0
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .workplane(offset=height)
    .circle(top_radius)
    .loft()
)
slot = (
    cq.Workplane("XY")
    .center(base_radius - slot_depth / 2, 0)
    .rect(slot_width, slot_depth)
    .loft()
)
result = base.cut(slot)
result = (
    result.faces(">Z")
    .workplane()
    .center(base_radius - slot_depth / 2, 0)
    .rect(slot_width, slot_depth)
    .cutBlind(-height)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(base_radius - slot_depth / 2, 0)
    .circle(mount_hole_diameter / 2)
    .cutBlind(-slot_depth)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(base_radius - slot_depth / 2, 0)
    .rect(slot_width, slot_depth)
    .cutBlind(-slot_depth)
)
