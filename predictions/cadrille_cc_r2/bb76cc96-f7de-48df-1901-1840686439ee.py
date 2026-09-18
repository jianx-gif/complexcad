import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=80.0,
    depth=30.0,
    height=12.0,
    arc_outer_diameter=100.0,
    top_fillet=2.0,
    top_fillet=2.0,
    hole_diameter=4.0,
    hole_spacing=15.0,
    hole_offset=10.0,
    hole_offset=20.0,
    hole_diameter=4.0,
    hole_spacing=15.0,
    hole_count=3,
    hole_count=4,
    hole_count=12
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)
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
    .fillet(m.top_fillet)
    .edges(">Z")
    .fillet(m.top_fillet)
)
result = (
    base
    .edges(">Z")
    .fillet(m.top_fillet)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (m.arc_center_radius, m.arc_center_radius**2),
        (-m.arc_center_radius, m.arc_center_radius**2),
        ( m.arc_center_radius, -m.arc_center_radius**2),
        ( m.arc_center_radius, -m.arc_center_radius**2),
    ])
    .hole(m.hole_diameter)
)
