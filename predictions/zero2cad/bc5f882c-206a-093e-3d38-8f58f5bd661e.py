import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=40.0,
    depth=12.0,
    height=15.0,
    arc_outer_diameter=80.0,
    slot_width=6.0,
    slot_length=30.0,
    slot_offset=5.0,
    chamfer=0.6,
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
    .chamfer(m.chamfer)
    .edges(">Z")
    .chamfer(m.chamfer)
    .faces(">Y")
    .workplane()
    .center(m.slot_offset, 0)
    .rect(m.slot_width, m.slot_length)
    .cutThruAll()
)
