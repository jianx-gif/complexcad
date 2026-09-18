import cadquery as cq
outer_diameter = 30.0
inner_diameter = 20.0
wall_thickness = 2.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = outer_diameter / 2.0
hole_offset = outer_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().fillet(fillet_radius)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
