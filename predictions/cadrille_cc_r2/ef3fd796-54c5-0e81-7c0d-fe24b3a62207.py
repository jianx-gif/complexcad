import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=60.0,
    depth=12.0,
    height=10.0,
    arc_outer_diameter=80.0,
    top_fillet=2.0,
    chamfer=0.5,
    hole_diameter=4.0,
    hole_spacing=20.0,
    hole_offset=20.0,
    hole_offset=20.0,
    hole_diameter=4.0,
    hole_depth=3.0,
    hole_spacing=15.0,
    hole_offset=20.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)
base = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path, transition="round")
    .edges("|Z")
    .chamfer(m.chamfer)
)
result = (
    base
    .edges(">Z")
    .fillet(m.top_fillet)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset, 0)
    .hole(m.hole_diameter)
)
