import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
thickness = 15.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
rib_count = 4
rib_offset = 10.0
chamfer_size = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius + rib_width, thickness)
    .lineTo(inner_radius + rib_width, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(rib_offset, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
