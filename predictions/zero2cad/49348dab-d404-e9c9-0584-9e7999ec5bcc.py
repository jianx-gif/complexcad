import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    width=60.0,
    depth=40.0,
    thickness=8.0,
    slot_width=12.0,
    slot_length=30.0,
    slot_depth=4.0,
    fillet_radius=2.0,
    chamfer_distance=0.5,
    hole_diameter=4.0,
    hole_spacing=30.0,
    hole_offset=10.0
)

result = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.slot_width, m.slot_length)
    .cutBlind(m.slot_depth)
    .edges("|X and >Z")
    .fillet(m.fillet_radius)
    .edges("|Y")
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .pushPoints([(-m.hole_spacing/2, 0), (m.hole_spacing/2, 0)])
    .hole(m.hole_diameter)
)
