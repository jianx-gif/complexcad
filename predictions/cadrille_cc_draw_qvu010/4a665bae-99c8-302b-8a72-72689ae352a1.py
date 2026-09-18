import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=30.0,
    depth=10.0,
    thickness=12.0,
    chamfer=1.0,
    hole_diameter=8.0,
    hole_spacing=12.0,
    hole_rows=2,
    hole_cols=3,
    hole_spacing=20.0,
    hole_diameter=12.0,
    hole_offset_x=15.0,
    hole_offset_y=10.0
)
m.outer = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
)
m.outer = (
    cq.Workplane("XY")
    .rect(m.width - m.depth, m.depth)
    .extrude(m.thickness)
)
result = m.outer.union(m.outer)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.depth, m.depth)
    .cutBlind(-m.thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.depth, m.depth)
    .cutBlind(-m.thickness)
)
