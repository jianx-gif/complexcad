import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=80.0,
    depth=30.0,
    thickness=10.0,
    arc_outer_diameter=12.0,
    rib_width=4.0,
    rib_height=2.0,
    rib_thickness=2.0,
    rib_spacing=12.0,
    rib_spacing=15.0,
    rib_count=4,
    rib_count=4,
    rib_count=5,
    chamfer=1.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_radius = 0.5 * m.arc_outer_diameter
m.arc_center_angle = degrees(acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)
base = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
base = base.cut(base)
base = base.edges("|Z").chamfer(m.chamfer)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .cutBlind(-m.rib_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
result = base.union(m)
