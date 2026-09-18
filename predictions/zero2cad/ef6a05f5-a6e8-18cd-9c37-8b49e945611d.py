import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    block_width = 60.0,
    block_height = 30.0,
    arc_radius = 40.0,
    revolve_angle = 120.0,
    chamfer_distance = 1.5,
    hole_diameter = 6.0,
    hole_depth = 20.0,
    hole_offset_x = 20.0,
    hole_offset_y = 10.0,
)

profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(m.block_width, 0)
    .lineTo(m.block_width, m.block_height)
    .radiusArc((0, m.block_height), m.arc_radius)
    .close()
)

result = (
    profile
    .revolve(m.revolve_angle)
    .edges()
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset_x, m.hole_offset_y)
    .hole(m.hole_diameter, depth=m.hole_depth)
)
