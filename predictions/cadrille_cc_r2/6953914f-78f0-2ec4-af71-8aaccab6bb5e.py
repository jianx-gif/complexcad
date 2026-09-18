import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 20
wall_thickness = 2
chamfer_distance = 2
hole_diameter = 5
hole_spacing = 12
hole_count = 6
hole_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, height)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, 0)
    .close()
    .revolve()
)
result = profile.revolve()
result = result.edges().chamfer(chamfer_distance)
result = result.faces(">Z").workplane().hole(hole_diameter)
result = result.faces(">Z").workplane().hole(hole_diameter)
