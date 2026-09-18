import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    linear_width = 80.0,
    depth = 60.0,
    height = 15.0,
    arc_outer_diameter = 100.0,
    arc_outer_radius = 30.0,
    arc_outer_radius = 8.0,
    chamfer_distance = 1.0,
    hole_diameter = 4.0,
    hole_depth = 8.0,
    hole_count = 6
)
m.arc_outer_radius = 0.5 * m.arc_outer_radius
m.arc_center_diameter = m.arc_outer_radius - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)
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
    .edges("|Z")
    .fillet(m.top_fillet)
    .edges(">Z")
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (m.arc_center_radius, 0),
        (-m.arc_center_radius, 0),
        (0, m.arc_center_radius),
        (0, -m.arc_center_radius)
    ])
    .hole(m.hole_diameter)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (m.arc_center_radius, 0),
        (-m.arc_center_radius, 0),
        (-m.arc_center_radius, 0)
    ])
    .hole(m.hole_diameter)
)
