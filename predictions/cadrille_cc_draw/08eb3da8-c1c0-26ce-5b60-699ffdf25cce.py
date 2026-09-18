import cadquery as cq
outer_radius = 20.0
inner_radius = 12.0
thickness = 30.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
rib_count = 4
rib_spacing = 15.0
chamfer_distance = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
