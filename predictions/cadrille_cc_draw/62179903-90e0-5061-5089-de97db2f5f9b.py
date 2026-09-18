import cadquery as cq
outer_radius = 30.0
inner_radius = 12.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 4
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + radi
    .close()
    .revolve()
)
result = profile.revolve()
