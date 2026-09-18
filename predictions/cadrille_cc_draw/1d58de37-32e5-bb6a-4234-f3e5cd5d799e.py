import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    plate_width=70.0,
    plate_depth=30.0,
    plate_thickness=5.0,
    rib_width=12.0,
    rib_height=15.0,
    rib_thickness=5.0,
    rib_offset_x=15.0,
    rib_offset_y=10.0,
    chamfer=0.5
)
m.arc_outer_radius = 0.5 * m.arc_outer_radius
m.arc_center_diameter = m.arc_outer_radius - m.rib_thickness
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.rib_width, m.rib_height)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(m.side_diameter)
    .edges(">Z")
    .chamfer(m.chamfer)
)
