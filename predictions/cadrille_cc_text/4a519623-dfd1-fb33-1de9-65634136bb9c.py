import cadquery as cq
overall_width = 80.0
overall_height = 60.0
length = 100.0
wall_thickness = 5.0
slot_width = 20.0
slot_height = 30.0
hole_diameter = 6.0
hole_spacing = 40.0
pocket_width = 30.0
pocket_length = 40.0
pocket_depth = 10.0
chamfer_size = 2.0
base = (
    cq.Workplane("XY")
    .rect(overall_width, overall_height)
    .extrude(length)
)
slot = (
    cq.Workplane("XY")
    .rect(slot_width, slot_height)
    .extrude(length)
)
slot = slot.edges("|Z").chamfer(chamfer_size)
slot = (
    slot.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_height)
    .cutBlind(-length)
)
slot = (
    slot.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_height)
    .cutBlind(-length)
)
slot = (
    slot.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_height)
    .cutBlind(-length)
)
result = slot
