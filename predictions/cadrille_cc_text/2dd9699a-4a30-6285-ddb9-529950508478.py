import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
mount_hole_diameter = 5.0
mount_hole_offset_x = 30.0
mount_hole_offset_y = 20.0
rib_width = 6.0
rib_height = 3.0
rib_spacing = 12.0
rib_count = 4
rib_count = 3
rib_spacing = 12.0
slot_width = 4.0
slot_length = 20.0
slot_offset_y = 25.0
fillet_radius = 1.5
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_height)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .polygon(6, mount_hole_diameter)
    .cutBlind(-mount_hole_offset_y)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .polygon(6, mount_hole_diameter)
    .cutBlind(-mount_hole_offset_y)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .polygon(6, mount_hole_diameter)
    .cutBlind(-plate_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .polygon(6, mount_hole_diameter)
    .cutBlind(-plate_thickness)
)
