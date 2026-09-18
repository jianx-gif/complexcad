import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
rib_count = 4
rib_count = 6
rib_radius = outer_diameter / 2.0
rib_height = thickness * 0.6
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, thickness * 0.6)
    .lineTo(inner_diameter / 2.0, thickness * 0.5)
    .lineTo(inner_diameter / 2.0, 0)
    .close()
)
solid = profile.revolve(360)
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(rib_radius, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
