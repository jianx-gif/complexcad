import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
wall_thickness = 5.0
inner_radius = outer_diameter / 2.0
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, inner_radius)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
