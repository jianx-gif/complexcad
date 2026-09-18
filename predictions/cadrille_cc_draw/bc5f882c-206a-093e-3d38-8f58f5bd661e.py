import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter = 60.0,
    height = 15.0,
    height = 12.0,
    arc_outer_diameter = 30.0,
    arc_outer_radius = 12.0,
    chamfer_distance = 1.0,
    hole_diameter = 5.0,
    hole_offset_x = 10.0,
    hole_offset_y = 15.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_radius
m.arc_center_diameter = m.arc_outer_diameter - m.arc_outer_radius - m.arc_outer_radius
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_diameter) / 2.0 * m.arc_center_angle)
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.arc_center_diameter / 2.0, 0.0), m.arc_center_angle)
    .wire()
)
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.arc_center_diameter, m.arc_center_diameter)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(m.fillet_radius)
    .edges(">Z")
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .center(m.arc_center_diameter / 2.0 - m.arc_center_diameter / 2.0, 0)
    .rect(m.arc_center_diameter, m.arc_center_diameter)
    .cutBlind(-m.arc_outer_radius)
    .faces(">Z")
    .workplane()
    .center(m.arc_center_diameter / 2.0 - m.arc_center_diameter / 2.0, 0)
    .rect(m.arc_center_diameter, m.arc_center_diameter)
    .cutBlind(-m.arc_outer_radius)
)
