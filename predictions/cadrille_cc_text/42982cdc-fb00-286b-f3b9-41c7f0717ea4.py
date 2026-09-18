import cadquery as cq
circle_diameter = 20.0
rect_width = 40.0
rect_height = 15.0
lever_length = 80.0
lever_width = 8.0
slot_width = 8.0
slot_length = 60.0
base_hole_diameter = 6.0
base_hole_spacing = 30.0
chamfer_dist = 2.0
base_hole_offset = base_hole_spacing / 2.0
base = (
    cq.Workplane("XY")
    .circle(circle_diameter / 2)
    .extrude(rect_height)
    .faces(">Z")
    .workplane()
    .hole(base_hole_diameter)
)
lever = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rect_width, lever_length)
    .extrude(rect_height)
    .translate((circle_diameter / 2 - base_hole_offset, 0, 0))
)
lever = lever.cut(lever)
lever = lever.edges("|Z").chamfer(chamfer_dist)
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_width, slot_length)
    .extrude(slot_length)
    .translate((circle_diameter / 2 - base_hole_offset, 0, 0))
)
lever = lever.cut(slot)
lever = lever.edges("|Z").chamfer(chamfer_dist)
result = lever
