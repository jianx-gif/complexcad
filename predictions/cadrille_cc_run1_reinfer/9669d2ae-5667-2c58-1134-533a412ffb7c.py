import cadquery as cq
outer_radius = 40.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_distance = 0.5
outer_profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, inner_radius)
    .close()
)
solid = outer_profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces('>Z').workplane().hole(inner_radius * 2)
solid = solid.faces('>Z').workplane().circle(inner_radius).cutBlind(-inner_radius)
solid = solid.faces('>Z').workplane().circle(inner_radius).extrude(inner_radius).translate((inner_radius + inner_radius, 0, 0))
solid = solid.edges('|Z').chamfer(chamfer_distance)
result = solid
