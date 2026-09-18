import cadquery as cq
import math
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter=80.0,
    outer_diameter=30.0,
    thickness=10.0,
    arc_outer_diameter=12.0,
    chamfer=0.5,
    hole_diameter=5.0,
    hole_depth=12.0,
    hole_offset=15.0,
    hole_offset_y=20.0,
    hole_offset_y=10.0,
    hole_offset_y=12.0,
    hole_offset_y=20.0,
    hole_offset_y=15.0,
    hole_offset_y=20.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_radius = 0.5 * m.arc_outer_diameter
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.arc_center_radius**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_diameter/2, 0.0), m.arc_center_radius)
    .wire()
)
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.rib_outer_diameter, m.rib_outer_diameter)
    .extrude(m.rib_height)
    .edges("|Z")
    .chamfer(m.chamfer)
)
