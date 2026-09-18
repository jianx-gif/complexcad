import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    arc_outer_diameter = 30.0,
    arc_outer_radius = 10.0,
    arc_height = 8.0,
    arc_offset = 12.0,
    chamfer_distance = 1.0,
    hole_diameter = 4.0,
    hole_spacing = 20.0,
    hole_offset = 10.0,
    hole_diameter = 6.0,
    hole_depth = 5.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_radius
m.arc_center_diameter = m.arc_outer_radius - m.arc_offset
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.arc_center_radius**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.arc_center_radius, 0.0), m.arc_center_radius)
    .wire()
)
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.arc_center_radius, m.arc_center_radius)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(m.fillet_radius)
    .edges(">Z")
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (m.arc_center_radius, 0.0),
        (-m.arc_center_radius, 0.0),
        (-m.arc_center_radius, 0.0),
        (0.5 * m.arc_center_radius, 0.0),
        (0.5 * m.arc_center_radius, 0.0),
        (-m.arc_center_radius, 0.0)
    ])
    .cboreHole(m.hole_diameter, m.hole_depth, m.hole_diameter)
)
