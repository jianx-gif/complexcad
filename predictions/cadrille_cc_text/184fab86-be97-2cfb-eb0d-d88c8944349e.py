import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=70.0,
    depth=12.0,
    height=20.0,
    arc_outer_diameter=100.0,
    chamfer_distance=0.5,
    tab_height=5.0,
    tab_width=2.5,
    tab_height=12.0,
    slot_length=8.0,
    slot_width=2.5,
    slot_width=5.0,
    slot_length=5.0,
    slot_width=10.0,
    slot_length=4.0,
    chamfer_distance=0.5,
)
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (m.linear_width, 0),
        (m.linear_width, m.depth),
        (m.linear_width, m.depth),
        (m.linear_width, m.depth),
        (0, m.depth),
    ])
    .close()
)
result = (
    profile
    .extrude(m.height)
    .edges("|Z")
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.slot_length, m.slot_width)
    .cutBlind(-m.height)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.slot_length, m.slot_width)
    .cutBlind(-m.height)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rarray(m.slot_length, 0, m.slot_width, 1)
    .rect(m.slot_length, m.slot_width)
    .cutBlind(-m.height)
    .edges("|Z")
    .chamfer(m.chamfer_distance)
)
