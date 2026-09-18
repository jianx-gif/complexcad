import cadquery as cq
overall_diameter = 60.0
wall_thickness = 4.0
rib_width = 10.0
rib_height = 2.0
mount_hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 45.0
mount_hole_diameter = mount_hole_diameter
mount_hole_count = 4
mount_hole_radius = overall_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(overall_diameter / 2.0, 0)
    .lineTo(overall_diameter / 2.0, rib_height)
    .lineTo(overall_diameter / 2.0, rib_height)
    .lineTo(overall_diameter / 2.0, rib_height)
    .lineTo(0, rib_height)
    .close()
)
result = profile.revolve()
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
    .cskHole(countersink_diameter, countersink_angle, mount_hole_count)
)
