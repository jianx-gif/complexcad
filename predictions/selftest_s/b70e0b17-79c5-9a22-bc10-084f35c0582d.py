import cadquery as cq
import math
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=60.0,
    depth=12.0,
    height=20.0,
    arc_outer_diameter=80.0,
    slot_width=30.0,
    slot_height=12.0,
    rib_width=25.0,
    rib_height=10.0,
    rib_thickness=4.0,
    edge_chamfer=0.5,
)

m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = math.degrees(
    math.acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2))
)
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
    # rectangular slot on top face
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.slot_width, m.slot_height)
    .cutBlind(-m.depth)
    # rib on bottom face
    .faces("<Z")
    .workplane(invert=True)
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
