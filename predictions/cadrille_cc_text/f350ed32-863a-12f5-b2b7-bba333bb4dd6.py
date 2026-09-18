import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=60.0,
    depth=30.0,
    thickness=6.0,
    nub_width=20.0,
    nub_height=2.0,
    nub_depth=10.0,
    slot_width=5.0,
    slot_length=45.0,
    slot_offset_y=8.0,
    hole_diameter=3.0,
    hole_spacing_x=40.0,
    hole_offset_y=10.0,
    outer_chamfer=0.5,
    hole_count=4,
    hole_depth=5.0,
)
base = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
    .edges("|Z")
    .fillet(m.top_fillet_radius)
    .faces(">Z")
    .workplane()
    .center(m.nut_offset_y, 0)
    .rect(m.nut_width, m.nut_height)
    .cutBlind(-m.thickness)
    .faces(">Z")
    .workplane()
    .center(m.nut_offset_y, 0)
    .hole(m.nut_diameter)
    .faces(">Z")
    .workplane()
    .center(m.nut_offset_y, 0)
    .rect(m.nut_width, m.nut_height)
    .cutBlind(-m.thickness)
    .faces(">Z")
    .workplane()
    .center(m.nut_offset_y, 0)
    .rect(m.nut_width, m.nut_height)
    .cutBlind(-m.thickness)
    .edges("|Z")
    .chamfer(m.outer_chamfer)
)
result = (
    base
    .faces(">Z")
    .workplane()
    .center(m.nut_offset_y, 0)
    .rect(m.nut_width, m.nut_height)
    .extrude(m.nut_depth)
)
