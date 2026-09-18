import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 2.0
rib_spacing = 12.0
rib_count = 6
fillet_radius = 0.5
chamfer_distance = 0.5
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().fillet(fillet_radius)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().fillet(fillet_radius)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
