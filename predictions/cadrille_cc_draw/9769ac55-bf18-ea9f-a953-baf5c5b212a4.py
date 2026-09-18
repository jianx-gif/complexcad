import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 15.0
rib_height = 10.0
rib_width = 6.0
rib_thickness = 4.0
rib_count = 8
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_offset = 10.0
rib_count = 4
rib_radius = outer_diameter / 2.0
rib_count = 3
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, thickness)
    .lineTo(outer_diameter / 2.0, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
