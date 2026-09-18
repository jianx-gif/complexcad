import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=60.0,
    depth=20.0,
    height=12.0,
    arc_outer_diameter=100.0,
    top_fillet=3.0,
    vertical_fillet=2.0,
    chamfer=0.8,
    slot_width=12.0,
    slot_height=8.0,
    slot_offset=5.0,
    pocket_width=30.0,
    pocket_depth=10.0,
    pocket_height=4.0,
    hole_spacing=30.0,
    hole_offset_y=5.0,
    bolt_diameter=4.0,
    head_diameter=8.0,
    head_height=3.0
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
    .edges("<Z")
    .chamfer(m.chamfer)
    .faces(">Z")
    .workplane()
    .center(0, m.slot_offset)
    .rect(m.slot_width, m.slot_height)
    .cutBlind(-m.height)
    .faces(">Z")
    .workplane()
    .center(0, -m.slot_offset)
    .rect(m.pocket_width, m.pocket_depth)
    .cutBlind(-m.pocket_height)
    .faces(">Z")
    .workplane()
    .center(-m.hole_spacing/2, m.hole_offset_y)
    .cboreHole(m.bolt_diameter, m.head_diameter, m.head_height)
    .center(m.hole_spacing, 0)
    .cboreHole(m.bolt_diameter, m.head_diameter, m.head_height)
)
