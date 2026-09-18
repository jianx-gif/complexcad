import cadquery as cq
base_width = 70.0
base_depth = 30.0
base_height = 5.0
clip_body_width = 20.0
clip_body_height = 15.0
clip_body_thickness = 4.0
rib_width = 5.0
rib_height = 3.0
rib_spacing = 8.0
mount_hole_dia = 6.0
mount_hole_spacing = 20.0
mount_hole_count = 4
mount_hole_spacing = 8.0
slot_width = 3.0
slot_spacing = 8.0
slot_rows = 2
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_height)
    .edges("|Z")
    .fillet(base_corner_radius)
)
clip_body = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(clip_body_width, clip_body_height)
    .cutBlind(-clip_body_thickness)
)
clip_body = (
    clip_body
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(mount_hole_dia / 2)
    .cutBlind(-clip_body_thickness)
)
clip_body = (
    clip_body
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_spacing)
    .cutBlind(-slot_spacing)
)
clip_body = (
    clip_body
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(mount_hole_dia / 2)
    .cutBlind(-clip_body_thickness)
)
result = clip_body
