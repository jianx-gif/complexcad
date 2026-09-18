import cadquery as cq
outer_radius = 25.0
inner_radius = 10.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
chamfer_size = 0.5
hole_diameter = 4.0
hole_depth = wall_thickness + 2.0
hole_count = 6
hole_circle_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + 2.0
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + 2.0
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + 2.0
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + 2.0
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + 2.0
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + 2.0)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + 2.0)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + 2.0)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + 2.0)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + 2.0)
    .close()
)
result = (
    profile
    .revolve()
    .edges()
    .chamfer(chamfer_size)
)
