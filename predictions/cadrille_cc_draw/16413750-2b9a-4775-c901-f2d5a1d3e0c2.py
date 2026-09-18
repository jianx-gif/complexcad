import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness + wall_thickness)
    .lineTo(inner_radius + wall_thickness + wall_thickness, wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + radi
    .close()
)
result = (
    profile
    .revolve()
    .shell(-wall_thickness)
    .edges()
    .chamfer(chamfer_size)
)
