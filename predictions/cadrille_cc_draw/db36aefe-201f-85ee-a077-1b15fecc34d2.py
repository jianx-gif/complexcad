import cadquery as cq
outer_radius = 15.0
inner_radius = 12.0
height = 2.0
rib_height = 4.0
rib_width = 6.0
rib_count = 8
rib_count = 4
rib_count = 6
rib_radius = outer_radius - rib_height
rib_count = 2
rib_count = 4
rib_count = 6
chamfer_size = 0.5
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height - rib_height)
    .lineTo(inner_radius, height - rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = outer_profile.revolve()
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
