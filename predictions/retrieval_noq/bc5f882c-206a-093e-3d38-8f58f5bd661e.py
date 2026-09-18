import cadquery as cq
import math
from types import SimpleNamespace as Measures

m = Measures(
    linear_width = 40.0,
    depth = 12.0,
    height = 12.0,
    arc_outer_diameter = 80.0,
    top_chamfer = 1.0,
    side_chamfer = 0.8,
    pocket_width = 20.0,
    pocket_depth = 6.0,
    pocket_height = 4.0,
    hole_spacing_x = 15.0,
    hole_spacing_y = 15.0,
    hole_rows = 2,
    hole_cols = 3,
    hole_clearance_diameter = 6.0,
    hole_depth = 6.0
)

m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)

path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)

sweep_profile = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
)

result = (
    sweep_profile
    .sweep(path, transition="round")
    .edges("|Z")
    .chamfer(m.side_chamfer)
    .edges(">Z")
    .chamfer(m.top_chamfer)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.pocket_width, m.pocket_depth)
    .cutBlind(-m.pocket_height)
    .faces(">Z")
    .workplane()
    .rarray(m.hole_spacing_x, m.hole_spacing_y, m.hole_cols, m.hole_rows, center=True)
    .hole(m.hole_clearance_diameter, depth=m.hole_depth)
)
