import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_size = 0.5
hole_diameter = 4.0
hole_depth = 12.0
hole_count = 8
hole_circle_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .close()
)
result = profile.revolve()
