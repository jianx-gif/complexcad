import cadquery as cq
from math import acos, degrees

class Measures:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

m = Measures(
    block_width=40.0,
    block_height=8.0,
    block_depth=12.0,
    arc_outer_diameter=80.0,
    fillet_radius=2.0,
    chamfer_distance=0.8,
    hole_diameter=4.0,
    hole_depth=5.0,
    hole_offset_x=20.0,
    hole_offset_y=6.0,
)

m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_radius = m.arc_outer_radius - m.block_depth
m.arc_center_angle = degrees(acos((2 * m.arc_center_radius**2 - m.block_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)

# Define sweep path: an arc centered at origin, ending at (block_width,0)
path = (
    cq.Workplane('XY')
    .radiusArc((m.block_width, 0.0), m.arc_center_radius)
    .wire()
)

# Build the block by sweeping a rectangle cross-section along the arc path
result = (
    cq.Workplane('XY')
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.block_depth, m.block_height)
    .sweep(path, transition='round')
    .edges('|Z')
    .fillet(m.fillet_radius)
    .edges('>Z')
    .chamfer(m.chamfer_distance)
    .faces('>Z')
    .workplane()
    .center(m.hole_offset_x, m.hole_offset_y)
    .hole(m.hole_diameter, depth=m.hole_depth)
)
