import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=60.0,
    depth=20.0,
    tslot_head_width=30.0,
    tslot_head_depth=4.0,
    tslot_stem_width=12.0,
    tslot_stem_height=18.0,
    tslot_stem_depth=12.0,
    chamfer=0.8,
)
m.arc_outer_diameter=95.0,
 m.arc_outer_radius=0.5,
 m.arc_outer_radius=0.0,
 m.arc_center_diameter=0.0,
 m.arc_center_radius=0.0,
 m.arc_height=3.0,
 m.arc_center_offset=0.0,
)
m.arc_center_angle= degrees(acos((2 * m.arc_center_diameter/2, 0), (2 * m.arc_center_radius, 0)]
m.arc_secant_angle = 0.5 * m.arc_center_diameter
m.arc_secant_angle = 0.5 * m.arc_center_diameter
m.arc_secant_angle = 0.5 * m.arc_center_diameter
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * (180 - m.arc_secant_angle)
m.arc_secant_angle = 0.5 * (180 - m.arc_secant_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_secant_angle)
    .wire()
)
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.depth)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(m.tape_secant_angle)
    .edges(">Z")
    .fillet(m.tape_secant_angle)
    .faces(">Z")
    .workplane()
    .center(m.taper_secant_angle/2, m.arc_secant_angle/2)
    .rect(m.taper_secant_angle, m.taper_secant_angle)
    .cutBlind(-m.depth)
    .edges(">Z")
    .fillet(m.taper_secant_angle)
)
