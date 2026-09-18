import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 2.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_distance = 0.5
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .close()
)
result = (
    outer_profile
    .revolve(360)
    .edges("|Z")
    .chamfer(chamfer_distance)
)
