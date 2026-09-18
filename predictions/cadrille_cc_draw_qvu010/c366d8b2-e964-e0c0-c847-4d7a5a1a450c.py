import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=60.0,
    depth=15.0,
    height=6.0,
    arc_outer_diameter=10.0,
    arc_outer_radius=15.0,
    chamfer_distance=1.0,
    hole_diameter=4.0,
    hole_spacing=12.0,
    hole_offset_x=15.0,
    hole_offset_y=10.0,
    hole_diameter=12.0,
    hole_offset_y=10.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_radius - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = degrees(acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)
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
    .fillet(m.toping_hole_diameter)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset_x, m.hole_offset_y)
    .hole(m.hole_diameter)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset_x, m.hole_offset_y)
    .hole(m.hole_diameter)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset_x, m.hole_offset_y)
    .hole(m.hole_diameter)
    .edges("|Z")
    .chamfer(m.chamfer_distance)
)
