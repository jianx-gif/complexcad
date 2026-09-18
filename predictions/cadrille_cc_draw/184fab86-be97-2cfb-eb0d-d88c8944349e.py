import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_radius=30.0,
    inner_radius=20.0,
    height=12.0,
    rib_width=12.0,
    rib_height=5.0,
    rib_thickness=5.0,
    rib_count=4,
    rib_spacing=15.0,
    rib_offset=15.0,
    rib_height=10.0,
    rib_count=4,
    rib_spacing=15.0,
    rib_offset=15.0,
    rib_height=10.0,
    rib_count=4,
    rib_spacing=15.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_radius
m.arc_center_radius = 0.5 * m.arc_outer_radius
m.arc_center_angle = degrees(acos((2 * m.arc_center_radius**2 - m.arc_center_radius**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.outer_radius, 0.0), m.arc_center_radius)
    .wire()
)
rib = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.rib_width, m.rib_height)
    .sweep(path, transition="round")
)
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
    .edges("|Z")
    .chamfer(m.chamfer)
)
