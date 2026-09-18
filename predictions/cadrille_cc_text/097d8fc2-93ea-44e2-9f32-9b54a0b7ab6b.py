import cadquery as cq
outer_radius = 40.0
wall_thickness = 3.0
cover_height = 10.0
fillet_radius = 1.5
mount_hole_dia = 4.0
rib_width = 4.0
rib_height = 2.0
rib_length = 20.0
rib_count = 4
rib_count = 3
rib_start_z = cover_height + 2 * rib_length
rib_end_z = cover_height + 2 * rib_start_z
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cover_height)
    .lineTo(0, cover_height)
    .close()
)
solid = profile.revolve()
solid = solid.shell(-wall_thickness)
solid = solid.faces(">Z").workplane().hole(mount_hole_dia)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges("|Z").fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(mount_hole_dia)
solid = solid.faces(">Z").workplane().hole(mount_hole_dia)
solid = solid.faces(">Z").workplane().rect(rib_width, rib_length).extrude(rib_height)
result = solid
