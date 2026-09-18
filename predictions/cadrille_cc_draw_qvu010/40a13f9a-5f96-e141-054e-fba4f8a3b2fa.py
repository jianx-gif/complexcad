import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_thickness = 2.0
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter/2, 0)
    .lineTo(inner_diameter/2, thickness)
    .lineTo(outer_diameter/2, thickness)
    .lineTo(outer_diameter/2, 0)
    .close()
)
solid = profile.revolve(36)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter/2, thickness/2)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
