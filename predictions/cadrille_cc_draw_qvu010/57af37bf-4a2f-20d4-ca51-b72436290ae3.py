import cadquery as cq
import math
outer_radius = 15.0
inner_radius = 10.0
thickness = 12.0
rib_width = 4.0
rib_height = 6.0
rib_thickness = 2.0
rib_count = 12
chamfer_distance = 0.5
profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(outer_radius, thickness + thickness)
    .lineTo(inner_radius, thickness + thickness + thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve(360)
solid = solid.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_width / 2, thickness / 2)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
