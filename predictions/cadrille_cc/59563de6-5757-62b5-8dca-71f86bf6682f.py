import cadquery as cq
outer_radius = 15
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
height = 30
rib_height = 5
rib_width = 10
rib_thickness = 2
rib_spacing = 12
chamfer_size = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, height - rib_height)
    .lineTo(inner_radius - rib_width, height - rib_height)
    .lineTo(inner_radius - rib_width, height - rib_height)
    .lineTo(inner_radius - rib_width, height - rib_height)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_thickness, rib_height)
    .translate((inner_radius - rib_width/2, 0, rib_height/2))
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
