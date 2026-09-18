import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=60.0,
    depth=15.0,
    height=15.0,
    arc_outer_diameter=100.0,
    flange_thickness=5.0,
    flange_outer_diameter=120.0,
    flange_recess_depth=3.0,
    flange_recess_diameter=20.0,
    chamfer=0.7,
    hole_diameter=4.0,
    hole_depth=8.0,
    hole_spacing=20.0,
    hole_offset=10.0
)

m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_radius = m.arc_outer_radius - m.depth
m.arc_center_angle = degrees(acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)

path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)

block = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path, transition="round")
)

flange = (
    block.faces("<Z")
    .workplane()
    .circle(m.flange_outer_diameter / 2)
    .extrude(m.flange_thickness)
)

flange = (
    flange.faces("<Z")
    .workplane()
    .circle(m.flange_recess_diameter / 2)
    .cutBlind(-m.flange_recess_depth)
)

flange = (
    flange.faces(">Z")
    .workplane()
    .center(-m.hole_spacing/2, m.hole_offset)
    .hole(m.hole_diameter, depth=m.hole_depth)
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter, depth=m.hole_depth)
)

result = block.union(flange)

result = result.edges(">Z").chamfer(m.chamfer)
