import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=60.0,
    depth=12.0,
    height=20.0,
    arc_outer_diameter=90.0,
    rib_thickness=2.0,
    rib_height=12.0,
    rib_offset=1.0,
    chamfer=0.5,
    hole_diameter=4.0,
    hole_depth=10.0,
    hole_offset_x=20.0,
    hole_offset_y=6.0,
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
    .polyline([
        (0, 0),
        (m.depth, 0),
        (m.depth, m.height),
        (m.depth/2, m.height + 5),
        (0, m.height),
    ])
    .close()
    .sweep(path, transition="round")
    .edges("|Z")
    .chamfer(m.chamfer)
)

rib = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .center(m.rib_offset, 0)
    .rect(m.rib_thickness, m.rib_height)
    .sweep(path, transition="round")
)

result = (
    base.union(rib)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset_x, m.hole_offset_y)
    .hole(m.hole_diameter, depth=m.hole_depth)
)
