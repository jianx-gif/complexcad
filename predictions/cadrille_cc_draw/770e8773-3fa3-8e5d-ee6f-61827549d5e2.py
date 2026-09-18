import cadquery as cq
outer_radius = 12.0
inner_radius = 12.0
height = 80.0
wall_thickness = 2.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 15.0
rib_count = 4
rib_count = 6
rib_count = 4
rib_count = 3
chamfer_size = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius + rib_width, height)
    .lineTo(inner_radius + rib_width, height + rib_height)
    .lineTo(inner_radius, height + rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_size)
result = solid
