import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=60.0,
    depth=12.0,
    height=15.0,
    arc_outer_diameter=100.0,
    rib_width=30.0,
    rib_height=10.0,
    rib_thickness=5.0,
    rib_spacing=12.0,
    rib_spacing=15.0,
    rib_spacing=12.0,
    rib_spacing=15.0,
    rib_spacing=12.0,
    rib_spacing=15.0,
    rib_spacing=12.0,
    rib_spacing=15.0,
    rib_spacing=20.0,
    rib_spacing=10.0,
    rib_spacing=15.0,
    rib_spacing=2.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_radius = 0.5 * m.arc_outer_radius
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)
base = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.rib_width, m.rib_spacing)
    .sweep(path, transition="round")
)
base = base.edges("|Z").fillet(m.fillet)
result = base
