import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
wall_thickness = 4.0
rib_height = 12.0
rib_width = 6.0
rib_thickness = 2.0
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2, 0)
    .lineTo(outer_diameter / 2, rib_height)
    .lineTo(outer_diameter / 2, rib_height)
    .lineTo(outer_diameter / 2, rib_height)
    .lineTo(outer_diameter / 2, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
