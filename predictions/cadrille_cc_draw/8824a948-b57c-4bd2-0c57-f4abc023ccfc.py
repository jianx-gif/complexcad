import cadquery as cq
import math
outer_diameter = 60.0
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
rib_height = thickness / 2.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, thickness)
    .lineTo(outer_diameter / 2.0, thickness + rib_height)
    .lineTo(outer_diameter / 2.0, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0, thickness + rib_height / 2.0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
