import cadquery as cq
from types import SimpleNamespace as Measures

params = Measures(
    linear_width=50.0,
    block_depth=15.0,
    block_height=12.0,
    arc_outer_diameter=100.0,
    key_slot_width=5.0,
    key_slot_depth=8.0,
    chamfer_distance=1.0
)

params.arc_outer_radius = 0.5 * params.arc_outer_diameter
params.arc_center_diameter = params.arc_outer_diameter - params.block_depth
params.arc_center_radius = 0.5 * params.arc_center_diameter
params.arc_center_angle = __import__('math').degrees(__import__('math').acos((2 * params.arc_center_radius**2 - params.linear_width**2) / (2 * params.arc_center_radius**2)))
params.arc_secant_angle = 0.5 * (180 - params.arc_center_angle)

arc_path = (
    cq.Workplane('XY')
    .radiusArc((params.linear_width, 0.0), params.arc_center_radius)
    .wire()
)

result = (
    cq.Workplane('XY')
    .transformed(rotate=(90, -params.arc_secant_angle, 0))
    .rect(params.block_depth, params.block_height)
    .sweep(arc_path, transition='round')
    .edges('|Z')
    .chamfer(params.chamfer_distance)
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(params.key_slot_width, params.block_height)
    .cutBlind(-params.block_depth)
)
