import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(outer_radius, inner_radius)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(inner_radius)
solid = solid.faces(">Z").workplane().hole(inner_radius)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").edges().chamfer(1.0)
result = solid
