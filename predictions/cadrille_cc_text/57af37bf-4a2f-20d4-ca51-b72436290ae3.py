import cadquery as cq
import math
from types import SimpleNamespace as Measures
params = Measures(
    outer_diameter=30.0,
    profile_height=20.0,
    central_bore_diameter=10.0,
    slot_height=5.0,
    slot_depth=5.0,
    chamfer_distance=1.0,
    slot_count=6,
    slot_count=6,
)
p = params
base = (
    cq.Workplane("XY")
    .circle(p.outer_diameter / 2)
    .extrude(p.outer_height)
)
base = base.edges().chamfer(p.chamfer_distance)
base = base.edges().chamfer(p.chamfer_distance)
slot = (
    cq.Workplane("XY")
    .center(p.outer_diameter / 2 + p.slot_count, 0)
    .rect(p.slot_depth, p.slot_height)
    .extrude(p.slot_depth)
)
base = base.cut(slot)
slot = (
    cq.Workplane("XY")
    .center(p.outer_diameter / 2 + p.slot_count, 0)
    .rect(p.slot_depth, p.slot_height)
    .extrude(p.slot_depth)
)
base = base.cut(slot)
slot = (
    cq.Workplane("XY")
    .center(p.outer_diameter / 2 + p.slot_count, 0)
    .rect(p.slot_depth, p.slot_height)
    .extrude(p.slot_depth)
)
base = base.cut(slot)
result = base
