import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=60.0,
    depth=15.0,
    height=12.0,
    arc_outer_diameter=100.0,
    top_fillet=2.0,
    vertical_fillet=1.5,
    pocket_width=30.0,
    pocket_depth=8.0,
    pocket_height=6.0,
    pocket_fillet=0.7,
    hole_diameter=4.0,
    hole_spacing=20.0,
    hole_offset=10.0
)

m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = degrees(acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)

path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)

result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(m.vertical_fillet)
    .edges(">Z")
    .fillet(m.top_fillet)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.pocket_width, m.pocket_depth)
    .cutBlind(m.pocket_height)
    .edges()
    .fillet(m.pocket_fillet)
    .faces(">Z")
    .workplane()
    .center(-m.hole_spacing/2, m.hole_offset)
    .hole(m.hole_diameter)
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter)
)
