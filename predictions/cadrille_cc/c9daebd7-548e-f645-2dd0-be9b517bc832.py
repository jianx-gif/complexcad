import cadquery as cq
outer_radius = 40.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, rib_height + rib_height)
    .lineTo(inner_radius, rib_height + rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = outer_profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_width)
    .translate((outer_radius - rib_width / 2, 0, rib_height / 2))
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
