import cadquery as cq
outer_diameter = 80.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - wall_thickness
chamfer_distance = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().circle(inner_radius).cutBlind(-inner_radius)
solid = solid.faces(">Z").workplane().circle(inner_radius).cutBlind(-inner_radius * 2)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
