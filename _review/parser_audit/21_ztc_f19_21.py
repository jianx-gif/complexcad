import cadquery as cq
from math import radians
from types import SimpleNamespace as Measures

m = Measures(
    block_width = 40.0,
    block_height = 20.0,
    arc_height = 8.0,
    sweep_angle = 120.0,
    chamfer_distance = 1.0,
    pocket_width = 15.0,
    pocket_depth = 8.0,
    pocket_thickness = 5.0,
    clearance_dia = 4.5,
    clearance_depth = 12.0,
    hole_offset_x = 12.0,
    hole_offset_y = 10.0,
)

profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(m.block_width, 0)
    .lineTo(m.block_width, m.block_height)
    .threePointArc((m.block_width/2, m.block_height + m.arc_height), (0, m.block_height))
    .close()
)

result = (
    profile
    .revolve(m.sweep_angle)
    .edges()
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset_x, m.hole_offset_y)
    .hole(m.clearance_dia, depth=m.clearance_depth)
    .faces("<Z")
    .workplane()
    .center(m.block_width/2, m.block_height/2)
    .rect(m.pocket_width, m.pocket_depth)
    .cutBlind(-m.pocket_thickness)
)
