import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
thickness = 10.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
rib_count = 4
rib_offset = 15.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius + rib_width, thickness)
    .lineTo(inner_radius + rib_width, rib_height)
    .lineTo(inner_radius + rib_width, rib_height + rib_height)
    .lineTo(inner_radius, rib_height + rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_width)
    .translate((inner_radius + rib_width/2, 0, rib_height/2))
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
