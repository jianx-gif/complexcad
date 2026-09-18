import cadquery as cq
from types import SimpleNamespace as Measures
from math import acos, degrees

m = Measures(
    chord_length = 50.0,
    sweep_depth = 12.0,
    sweep_height = 15.0,
    outer_diameter = 80.0,
    wall_thickness = 2.0,
    blind_hole_diameter = 6.0,
    blind_hole_depth = 8.0,
    clearance_hole_diameter = 4.0,
    chamfer_distance = 0.5,
)

m.outer_radius = 0.5 * m.outer_diameter
m.inner_radius = m.outer_radius - m.sweep_depth
m.arc_center_angle = degrees(acos((2 * m.inner_radius**2 - m.chord_length**2) / (2 * m.inner_radius**2)))
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)

path = (
    cq.Workplane("XY")
    .radiusArc((m.chord_length, 0.0), m.inner_radius)
    .wire()
)

result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.sweep_depth, m.sweep_height)
    .sweep(path, transition="round")
    .shell(m.wall_thickness)
    .edges("|Z")
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(m.blind_hole_diameter / 2)
    .cutBlind(m.blind_hole_depth)
    .faces(">X")
    .workplane()
    .hole(m.clearance_hole_diameter)
)
