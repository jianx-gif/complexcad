import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
wall_thickness = 2.0
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(outer_radius, 0)
    .close()
    .revolve()
)
result = profile.revolve()
result = result.edges().fillet(inner_radius)
result = result.faces(">Z").edges().chamfer(outer_diameter)
result = result.faces(">Z").edges().fillet(inner_radius)
