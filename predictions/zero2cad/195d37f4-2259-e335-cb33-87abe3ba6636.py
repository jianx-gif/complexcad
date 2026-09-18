import cadquery as cq
import math
outer_radius = 45.0
inner_radius = 20.0
block_height = 30.0
arc_angle = 150.0
groove_width = 5.0
groove_depth = 2.0
groove_center_z = block_height / 2.0
chamfer_size = 0.5
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .threePointArc((outer_radius, block_height / 2.0), (inner_radius, block_height))
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve(arc_angle)
# Groove cutter cylinder
groove_cutter = (
    cq.Workplane("XY")
    .center(outer_radius - groove_depth / 2.0, 0)
    .circle(groove_width / 2.0)
    .extrude(block_height)
    .translate((0, 0, groove_center_z - block_height / 2.0))
)
result = solid.cut(groove_cutter).edges().chamfer(chamfer_size)
