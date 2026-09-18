import cadquery as cq
outer_radius = 40.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_height = 12.0
rib_width = 6.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
mount_hole_dia = 4.0
mount_hole_offset = 10.0
rib_count = 6
rib_width = 12.0
rib_height = 10.0
rib_spacing = 15.0
rib_count = 8
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, outer_radius)
    .lineTo(outer_radius + rib_width, outer_radius)
    .lineTo(outer_radius + rib_width, outer_radius + rib_height)
    .lineTo(outer_radius, outer_radius + rib_height)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
