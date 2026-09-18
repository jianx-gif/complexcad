import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(inner_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
result = solid
