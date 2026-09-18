import cadquery as cq
outer_radius = 40.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_height = 10.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_width)
    .translate((inner_radius + rib_width / 2, 0, rib_height / 2))
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_size)
solid = (
    solid.faces(">Z")
    .workplane()
    .center(inner_radius + wall_thickness / 2, 0)
    .hole(inner_radius * 2)
)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
