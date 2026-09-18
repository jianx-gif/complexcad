import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=80.0,
    depth=60.0,
    height=20.0,
    wall_thickness=4.0,
    corner_radius=5.0,
    chamfer=1.0,
    hole_diameter=20.0,
    hole_count=4,
    hole_spacing=15.0,
    hole_count=4,
    hole_offset=0.0
)
m.arc_angle = 0.5 * m.arc_angle
m.arc_center_angle = 0.5 * m.arc_angle
m.arc_center_angle = 0.5 * m.arc_angle
m.arc_center_angle = 0.5 * m.arc_angle
m.arc_secant_angle = 0.5 * m.arc_angle
m.arc_secant_angle = 0.5 * m.arc_center_angle
m.arc_secant_angle = 0.5 * m.arc_center_angle
m.arc_secant_angle = 0.5 * m.arc_center_angle
m.arc_secant_angle = 0.5 * m.arc_center_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * m.arc_secant_angle
m.arc_secant_angle = 0.5 * (180 - m.arc_secant_angle)
m.arc_secant_angle = 0.5 * (180 - m.arc_secant_angle)
m.arc_secant_angle = 0.5 * (180 - m.arc_secant_angle)
path = (
    cq.Workplane("XY")
    .polyline(m.m.arc_secant_angle, m.arc_secant_angle)
    .close()
    .extrude(m.depth)
)
result = (
    cq.Workplane("XY")
    .polyline(m.m.hole_diameter, m.hole_count)
    .close()
    .extrude(m.depth)
)
