import cadquery as cq
from types import SimpleNamespace as Measures
from math import sin, radians

# Base parameters
m = Measures(
    block_depth=10.0,
    block_height=15.0,
    arc_center_radius=30.0,
    arc_angle_deg=120.0,
    chamfer_distance=2.0,
    hole_diameter=4.0,
    hole_spacing_x=20.0,
    hole_spacing_y=20.0,
    holes_per_row=2,
    holes_per_col=2,
)

# Derived dimensions
m.arc_angle_rad = radians(m.arc_angle_deg)
# chord length (linear width) corresponding to the arc angle
m.linear_width = 2 * m.arc_center_radius * sin(m.arc_angle_rad / 2)
# secant angle needed for proper orientation of the sweep cross‑section
m.arc_secant_angle = 0.5 * (180.0 - m.arc_angle_deg)

# Create the arc path for the sweep
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)

result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.block_depth, m.block_height)
    .sweep(path, transition="round")
    .edges("|Z")
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .rarray(m.hole_spacing_x, m.hole_spacing_y, m.holes_per_row, m.holes_per_col, center=True)
    .hole(m.hole_diameter)
)
