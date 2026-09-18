import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=50.0,
    depth=18.0,
    height=14.0,
    arc_outer_diameter=100.0,
    vertical_fillet=1.0,
    top_fillet=1.0,
    chamfer=0.5,
    boss_diameter=15.0,
    boss_height=5.0,
    tap_diameter=4.5,
    tap_depth=8.0,
    rib_width=4.0,
    rib_height=3.0,
    rib_offset=20.0
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
    .fillet(m.vertical_fillet)
    .edges(">Z")
    .fillet(m.top_fillet)
    .edges("<Z")
    .chamfer(m.chamfer)
)

rib = (
    cq.Workplane("XY")
    .center(m.rib_offset, 0)
    .rect(m.rib_width, m.height)
    .extrude(m.rib_height)
)

boss = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .circle(m.boss_diameter / 2)
    .extrude(m.boss_height)
)

result = base.union(rib).union(boss)

result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .hole(m.tap_diameter, depth=m.tap_depth)
)
