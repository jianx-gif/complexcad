import cadquery as cq
cover_length = 80.0
cover_width = 60.0
cover_thickness = 8.0
wall_thickness = 2.0
fillet_radius = 2.0
chamfer_dist = 1.5
slot_width = 12.0
slot_leg_length = 30.0
slot_leg_height = 25.0
slot_leg_length = 30.0
mount_hole_dia = 5.0
mount_hole_spacing_x = 40.0
mount_hole_spacing_y = 30.0
rib_width = 10.0
rib_height = 4.0
rib_spacing = 15.0
result = (
    cq.Workplane("XY")
    .rect(cover_length, cover_width)
    .extrude(cover_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(cover_length - 2 * wall_thickness, cover_width - 2 * wall_thickness)
    .cutBlind(-cover_thickness)
)
slot_cut = (
    result
    .faces(">Z")
    .workplane()
    .rect(slot_leg_length, slot_leg_height)
    .cutBlind(-slot_leg_height)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(cover_length - 2 * wall_thickness, cover_width - 2 * wall_thickness)
    .cutBlind(-cover_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_spacing)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_spacing)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_spacing)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_spacing)
)
