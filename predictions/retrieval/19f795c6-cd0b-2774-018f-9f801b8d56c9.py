import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=60.0,
    depth=20.0,
    height=15.0,
    arc_outer_diameter=90.0,
    shell_thickness=3.0,
    chamfer_distance=2.0,
    hole_diameter=5.0,
    hole_spacing=30.0
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
    .shell(-m.shell_thickness)
    .edges()
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-m.hole_spacing/2, -m.hole_spacing/2),
        ( m.hole_spacing/2, -m.hole_spacing/2),
        (-m.hole_spacing/2,  m.hole_spacing/2),
        ( m.hole_spacing/2,  m.hole_spacing/2)
    ])
    .hole(m.hole_diameter)
)
