import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=70.0,
    depth=20.0,
    height=10.0,
    arc_outer_diameter=80.0,
    rib_width=4.0,
    rib_height=12.0,
    rib_thickness=5.0,
    rib_spacing=15.0,
    chamfer=0.5,
    hole_diameter=4.0,
    hole_spacing=30.0,
    hole_offset=0.0,
    hole_offset=15.0,
    hole_offset_y=0.0
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
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
    .edges("|Z")
    .chamfer(m.chamfer)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset, 0)
    .hole(m.hole_diameter)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset, 0)
    .hole(m.hole_diameter)
    .center(m.hole_offset, 0)
    .hole(m.hole_diameter)
)
