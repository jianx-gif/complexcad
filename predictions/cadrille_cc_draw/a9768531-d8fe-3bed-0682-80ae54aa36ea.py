import cadquery as cq
import math
outer_diameter = 30.0
inner_diameter = 20.0
thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
chamfer_distance = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2, 0)
    .lineTo(outer_diameter / 2, 0)
    .lineTo(outer_diameter / 2, thickness)
    .lineTo(outer_diameter / 2, thickness + thickness)
    .lineTo(outer_diameter / 2, 0)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2 + rib_spacing / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
