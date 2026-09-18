import cadquery as cq
import math
from types import SimpleNamespace as Measures
m = Measures(
    block_width=10.0,
    block_height=30.0,
    block_height=15.0,
    arc_outer_diameter=10.0,
    arc_outer_radius=15.0,
    arc_outer_radius=8.0,
    arc_outer_radius=3.0,
    arc_outer_radius=2.0,
    chamfer_distance=1.0,
    hole_diameter=4.0,
    hole_spacing=12.0
)
base = (
    cq.Workplane("XY")
    .rect(m.block_width, m.block_height)
    .extrude(m.block_height)
)
base = base.edges().chamfer(m.chamfer_distance)
base = base.edges().chamfer(m.chamfer_distance)
base = (
    base.faces(">Z")
    .workplane()
    .center(m.block_width/2 - m.block_height/2, 0)
    .rect(m.block_width, m.block_height)
    .cutBlind(-m.block_height)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(m.block_width/2 - m.block_height/2, 0)
    .rect(m.block_width, m.block_height)
    .cutBlind(-m.block_height)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter)
)
result = base
