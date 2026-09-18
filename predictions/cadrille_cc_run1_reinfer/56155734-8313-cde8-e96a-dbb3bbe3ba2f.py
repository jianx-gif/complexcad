import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=60.0,
    depth=30.0,
    height=12.0,
    arc_outer_diameter=80.0,
    top_fillet=2.0,
    top_fillet=2.0,
    top_fillet=4.0,
    chamfer=1.0,
    hole_diameter=4.0,
    hole_spacing=20.0,
    hole_rows=2,
    hole_cols=3,
    hole_spacing_x=20.0,
    hole_spacing_y=15.0,
    hole_spacing_y=10.0,
    hole_spacing_y=15.0,
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
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
    .fillet(m.side_fillet)
    .edges(">Z")
    .fillet(m.top_fillet)
    .faces(">Z")
    .workplane()
    .center(m.hole_spacing_x, m.hole_spacing_y)
    .hole(m.hole_diameter)
    .faces(">Z")
    .workplane()
    .center(m.hole_spacing_x, m.hole_spacing_y)
    .hole(m.hole_diameter)
    .edges(">Z")
    .chamfer(m.chamfer)
)
