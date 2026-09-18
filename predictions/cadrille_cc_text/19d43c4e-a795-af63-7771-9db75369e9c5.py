import cadquery as cq
base_width = 80.0
base_length = 60.0
spacer_thickness = 8.0
corner_radius = 4.0
central_hole_diameter = 20.0
slot_width = 6.0
slot_length = 15.0
slot_depth = 4.0
slot_spacing_x = 20.0
slot_spacing_y = 20.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_width, base_length)
    .extrude(spacer_thickness)
)
slot_center_x = -base_width/2 + slot_width/2
slot_center_y = -base_length/2 + slot_spacing_y/2
slot = (
    cq.Workplane("XY")
    .center(slot_center_x, slot_center_y)
    .rect(slot_width, slot_length)
    .extrude(spacer_thickness)
)
base = base.union(slot)
base = base.edges("|Z").fillet(corner_radius)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(spacer_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(central_hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(spacer_thickness)
)
result = base
