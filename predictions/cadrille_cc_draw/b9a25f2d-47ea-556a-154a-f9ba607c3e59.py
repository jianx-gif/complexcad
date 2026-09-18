import cadquery as cq
import math
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=50.0,
    depth=10.0,
    height=12.0,
    arc_outer_diameter=80.0,
    top_fillet=1.0,
    hole_diameter=4.0,
    hole_offset_x=15.0,
    hole_offset_y=12.0,
    chamfer=0.5,
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_radius = m.arc_outer_radius - m.depth
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.depth)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(m.fillet)
    .edges(">Z")
    .fillet(m.fillet)
    .edges(">Z")
    .chamfer(m.chamfer)
)
