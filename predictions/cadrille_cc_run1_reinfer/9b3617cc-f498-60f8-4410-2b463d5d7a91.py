import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
wall_thickness = 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - wall_thickness
chamfer_distance = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().circle(inner_radius).cutBlind(-inner_radius * 2)
solid = solid.faces(">Z").workplane().circle(inner_radius).cutBlind(-inner_radius * 2)
solid = solid.faces(">Z").workplane().polarArray(radius=inner_radius - wall_thickness/2, count=4, startAngle=0, angle=360).hole(inner_radius * 2)
result = solid
