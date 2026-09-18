import cadquery as cq
from types import SimpleNamespace as Measures
from math import acos, degrees

# Parameters
p = Measures(
    block_width=60.0,
    block_depth=20.0,
    block_height=25.0,
    arc_diameter=100.0,
    cutout_radius=20.0,
    chamfer_dist=1.0,
    hole_offset_x=15.0,
    hole_offset_y=10.0,
    bolt_diameter=4.0,
    head_diameter=7.0,
    head_height=3.5,
)

# Derived geometry
p.arc_center_radius = 0.5 * p.arc_diameter
p.arc_center_angle = degrees(acos((2 * p.arc_center_radius**2 - p.block_width**2) / (2 * p.arc_center_radius**2)))
p.arc_secant_angle = 0.5 * (180 - p.arc_center_angle)

# Path for sweep (arc)
path = (
    cq.Workplane("XY")
    .radiusArc((p.block_width, 0), p.arc_center_radius)
    .wire()
)

# Base block created by sweeping a rectangle along the arc
base = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -p.arc_secant_angle, 0))
    .rect(p.block_depth, p.block_height)
    .sweep(path, transition="round")
    .edges("|Z")
    .chamfer(p.chamfer_dist)
    .edges(">Z")
    .chamfer(p.chamfer_dist)
)

# Semi‑circular cutout (half‑cylinder intersected with a box)
# Full cylinder oriented along +X
cyl = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 90, 0))
    .center(0, 0)
    .circle(p.cutout_radius)
    .extrude(p.block_depth + 2)
)
# Box to keep only the lower half of the cylinder
box = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 90, 0))
    .box(p.block_depth + 2, p.cutout_radius * 2, p.cutout_radius)
    .translate((0, 0, -p.cutout_radius / 2))
)
half_cyl = cyl.intersect(box)

# Apply cutout
model_with_cut = base.cut(half_cyl)

# Add tapped hole on the front face
result = (
    model_with_cut
    .faces("<X")
    .workplane()
    .center(p.hole_offset_x, p.hole_offset_y)
    .cboreHole(p.bolt_diameter, p.head_diameter, p.head_height)
)
