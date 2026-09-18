import cadquery as cq
from types import SimpleNamespace as Measures
params = Measures(
    linear_width=60.0,
    block_height=10.0,
    block_depth=12.0,
    arc_outer_diameter=100.0,
    arc_outer_diameter=30.0,
    arc_outer_diameter=5.0,
    arc_depth=15.0,
    arc_angle=50.0,
    chamfer_distance=0.8,
)
params.arc_outer_radius = params.arc_outer_diameter / 2.0
params.arc_center_radius = params.arc_outer_diameter / 2.0
params.arc_center_angle = degrees(acos((2 * params.arc_center_radius**2 - params.arc_center_radius**2) / (2 * params.arc_center_radius**2)))
params.arc_secant_angle = 0.5 * (180 - params.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((params.arc_outer_radius, 0.0), params.arc_center_radius)
    .wire()
)
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -params.arc_secant_angle, 0))
    .rect(params.height, params.height)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(params.fillet)
    .edges(">Z")
    .fillet(params.fillet)
    .faces(">Z")
    .workplane()
    .center(params.height/2, params.height/2)
    .rect(params.height, params.height)
    .cutBlind(params.height)
    .edges("|Z")
    .fillet(params.fillet)
    .edges(">Z")
    .chamfer(params.chamfer_distance)
)
