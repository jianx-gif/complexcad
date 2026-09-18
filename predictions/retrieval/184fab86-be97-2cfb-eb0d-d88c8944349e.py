import cadquery as cq
import math
from types import SimpleNamespace as NS

meas = NS(
    arc_radius=40.0,
    arc_angle=120.0,
    thickness=15.0,
    height=20.0,
    counterbore_diameter=30.0,
    counterbore_depth=5.0,
    fillet_radius=2.0,
    rib_width=5.0,
    rib_depth=3.0,
    rib_offset=3.0,
    hole_diameter=6.0,
    hole_spacing=20.0,
    hole_offset=10.0,
)

meas.linear_width = 2 * meas.arc_radius * math.sin(math.radians(meas.arc_angle / 2.0))
meas.secant_angle = (180.0 - meas.arc_angle) / 2.0

path = (
    cq.Workplane("XY")
    .radiusArc((meas.linear_width, 0.0), meas.arc_radius)
    .wire()
)

result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -meas.secant_angle, 0))
    .rect(meas.thickness, meas.height)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(meas.fillet_radius)
    .edges(">Z")
    .fillet(meas.fillet_radius)
)

# internal rib pocket on the flat side
result = (
    result
    .faces(">Y")
    .workplane()
    .center(meas.rib_offset, 0)
    .rect(meas.rib_width, meas.rib_depth)
    .cutBlind(-meas.rib_depth)
)

# peripheral counterbore on the top face
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(meas.counterbore_diameter / 2.0)
    .cutBlind(-meas.counterbore_depth)
)

# two mounting cbore holes
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-meas.hole_spacing / 2.0, meas.hole_offset)
    .cboreHole(meas.hole_diameter, meas.hole_diameter * 1.5, meas.hole_diameter / 2.0)
    .center(meas.hole_spacing, 0)
    .cboreHole(meas.hole_diameter, meas.hole_diameter * 1.5, meas.hole_diameter / 2.0)
)
