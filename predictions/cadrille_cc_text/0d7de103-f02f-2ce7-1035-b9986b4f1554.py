import cadquery as cq
base_width = 60.0
base_height = 30.0
base_depth = 12.0
wall_thickness = 1.5
corner_radius = 4.0
slot_width = 4.0
slot_length = 20.0
slot_offset = 8.0
chamfer_size = 0.8
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_depth)
    .faces(">Z")
    .workplane()
    .circle(corner_radius)
    .cutBlind(corner_depth)
)
slot = (
    base.faces(">Z")
    .workplane()
    .rect(slot_width, slot_length)
    .cutBlind(slot_depth)
)
result = (
    slot
    .faces(">Z")
    .workplane()
    .center(slot_offset, 0)
    .rect(slot_width, slot_length)
    .cutBlind(corner_depth)
)
result = result.edges("|Z").chamfer(chamfer_size)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, slot_offset)
    .rect(slot_width, slot_length)
    .cutBlind(corner_depth)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, slot_offset)
    .rect(slot_width, slot_length)
    .cutBlind(corner_depth)
)
