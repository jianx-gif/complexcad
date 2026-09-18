import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

p = Measures(
    linear_width=45.0,
    depth=12.0,
    height=14.0,
    outer_diameter=90.0,
    top_fillet=2.5,
    flat_face_width=30.0,
    flat_face_height=10.0,
    flat_face_depth=2.0,
    groove_width=4.0,
    groove_depth=6.0,
    groove_margin=2.0
)

p.outer_radius = 0.5 * p.outer_diameter
p.inner_radius = p.outer_radius - p.depth
p.arc_center_angle = degrees(acos((2 * p.inner_radius ** 2 - p.linear_width ** 2) / (2 * p.inner_radius ** 2)))
p.arc_secant_angle = 0.5 * (180 - p.arc_center_angle)

arc_path = (
    cq.Workplane("XY")
    .radiusArc((p.linear_width, 0.0), p.inner_radius)
    .wire()
)

base_block = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -p.arc_secant_angle, 0))
    .rect(p.depth, p.height)
    .sweep(arc_path, transition="round")
    .edges(">Z")
    .fillet(p.top_fillet)
)

flat_face = (
    base_block
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(p.flat_face_width, p.flat_face_height)
    .cutBlind(-p.flat_face_depth)
)

groove = (
    flat_face
    .faces("<X")
    .workplane()
    .center(0, 0)
    .rect(p.groove_width, p.height - 2 * p.groove_margin)
    .cutBlind(-p.groove_depth)
)

result = groove