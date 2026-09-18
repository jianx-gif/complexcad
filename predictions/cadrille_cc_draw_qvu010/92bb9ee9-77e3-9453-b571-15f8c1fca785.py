import cadquery as cq
outer_radius = 40.0
inner_radius = 30.0
wall_thickness = 10.0
rib_height = 20.0
rib_width = 12.0
rib_thickness = 4.0
rib_count = 8
chamfer_distance = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 15.0
rib_count = 6
rib_width = 10.0
rib_height = 8.0
rib_offset = 12.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height + rib_height)
    .lineTo(outer_radius, rib_height + rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.edges("|Z").chamfer(chamfer_distance)
result = solid
