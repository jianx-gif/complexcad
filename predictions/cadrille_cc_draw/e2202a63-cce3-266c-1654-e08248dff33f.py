import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 8.0
rib_height = 40.0
rib_thickness = 6.0
rib_spacing = 12.0
rib_count = 6
chamfer_distance = 1.0
mount_hole_dia = 5.0
mount_hole_offset = 15.0
rib_count = 4
rib_radius = outer_diameter / 2.0
rib_count = 3
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, rib_thickness)
    .lineTo(outer_diameter / 2.0, rib_thickness)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, rib_thickness + rib_height)
    .lineTo(outer_diameter / 2.0, 0)
    .close()
)
result = (
    profile
    .revolve()
    .edges()
    .chamfer(chamfer_distance)
)
