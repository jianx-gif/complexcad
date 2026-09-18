import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    arc_outer_diameter = 80.0,
    linear_width = 50.0,
    block_depth = 12.0,
    block_height = 15.0,
    wall_thickness = 2.0,
    relief_length = 6.0,
    relief_width = 8.0,
    fillet_radius = 2.0,
    chamfer_distance = 0.5,
    hole_spacing = 20.0,
    hole_diameter = 4.0,
    hole_depth = 5.0
)

m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_inner_radius = m.arc_outer_radius - m.block_depth
m.arc_center_angle = degrees(acos((2 * m.arc_inner_radius**2 - m.linear_width**2) / (2 * m.arc_inner_radius**2)))
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)

path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_inner_radius)
    .wire()
)

solid = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.block_depth, m.block_height)
    .sweep(path, transition="round")
)

thin = solid.shell(-m.wall_thickness)

result = (
    thin
    .edges("|Z").fillet(m.fillet_radius)
    .edges(">Z").chamfer(m.chamfer_distance)
    .faces(">X").workplane()
    .center(0, 0)
    .rect(m.relief_length, m.relief_width)
    .cutBlind(-2 * m.wall_thickness)
    .faces("<Z").workplane()
    .pushPoints([(-m.hole_spacing/2, 0), (m.hole_spacing/2, 0)])
    .hole(m.hole_diameter)
)
