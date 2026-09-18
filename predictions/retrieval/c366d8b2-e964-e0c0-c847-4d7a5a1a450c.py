import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

m = Measures(
    linear_width=55.0,
    depth=12.0,
    height=12.0,
    arc_outer_diameter=95.0,
    top_fillet=3.0,
    side_fillet=2.0,
    chamfer=0.5,
    hole_grid_rows=2,
    hole_grid_cols=3,
    hole_spacing_x=20.0,
    hole_spacing_y=15.0,
    hole_diameter=4.8,
    hole_offset_x=10.0,
    hole_offset_y=8.0,
)

m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = degrees(acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)

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
    # add a recessed pocket to increase profile complexity
    .center(m.depth/2, 0)
    .rect(m.depth/3, m.height/2)
    .cutBlind(m.height/4)
    # tapped hole array (clearance holes intended for tapping)
    .faces(">Z")
    .workplane()
    .center(m.hole_offset_x, m.hole_offset_y)
    .rarray(m.hole_spacing_x, m.hole_spacing_y, m.hole_grid_cols, m.hole_grid_rows)
    .hole(m.hole_diameter)
    .edges("|Z")
    .chamfer(m.chamfer)
)
