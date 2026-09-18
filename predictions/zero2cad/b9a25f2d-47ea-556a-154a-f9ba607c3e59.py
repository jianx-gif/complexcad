import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=55.0,
    depth=12.0,
    height=10.0,
    arc_outer_diameter=100.0,
    rib_width=20.0,
    rib_height=8.0,
    rib_thickness=5.0,
    chamfer=0.8,
    hole_diameter=4.0,
    hole_spacing=12.0,
    hole_count=3,
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

base = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path, transition="round")
    .edges("|Z")
    .chamfer(m.chamfer)
    .edges(">Z")
    .chamfer(m.chamfer)
)

rib = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)

result = (
    rib.faces(">Z").workplane()
    .center(-((m.hole_count - 1) * m.hole_spacing) / 2, 0)
    .rarray(m.hole_spacing, 0, m.hole_count, 1)
    .hole(m.hole_diameter)
    .edges(">Z")
    .chamfer(m.chamfer / 2)
)
