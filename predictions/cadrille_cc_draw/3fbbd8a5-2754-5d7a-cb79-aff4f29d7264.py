import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 30.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_spacing = 20.0
rib_count = 4
rib_radius = outer_diameter / 2.0
rib_height = thickness * rib_height
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
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_size)
result = solid
