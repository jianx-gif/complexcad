import cadquery as cq
spacer_width = 60.0
spacer_length = 40.0
spacer_thickness = 12.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 10.0
counterbore_diam = 15.0
counterbore_depth = 6.0
chamfer_size = 1.0
key_slot_width = 8.0
key_slot_depth = 5.0
key_slot_depth = 5.0
base = (
    cq.Workplane("XY")
    .rect(spacer_width, spacer_length)
    .extrude(spacer_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, spacer_length)
    .extrude(rib_height)
    .translate((0, 0, spacer_thickness))
)
result = base.union(rib)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(counterbore_diam, depth=counterbore_depth)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(counterbore_diam, depth=counterbore_depth)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(counterbore_diam, depth=counterbore_depth)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(key_slot_width, key_slot_depth)
    .cutBlind(-spacer_thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(counterbore_diam, depth=counterbore_depth)
)
result = result.edges("|Z").chamfer(chamfer_size)
