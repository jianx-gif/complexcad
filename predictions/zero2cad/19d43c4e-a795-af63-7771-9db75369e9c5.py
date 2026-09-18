import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    width=80.0,
    depth=60.0,
    thickness=8.0,
    corner_radius=4.0,
    central_hole_dia=20.0,
    slot_width=6.0,
    slot_length=30.0,
    slot_offset=12.0,
    chamfer=1.0,
)

result = (
    cq.Workplane('XY')
    .rect(m.width, m.depth)
    .extrude(m.thickness)
    .edges('|Z')
    .fillet(m.corner_radius)
    .edges('>Z')
    .chamfer(m.chamfer)
    .faces('>Z')
    .workplane()
    .hole(m.central_hole_dia)
    .faces('>Z')
    .workplane()
    .center(0, m.depth/2 - m.slot_offset)
    .rect(m.slot_length, m.slot_width)
    .cutBlind(m.thickness)
    .faces('>Z')
    .workplane()
    .center(0, -(m.depth/2 - m.slot_offset))
    .rect(m.slot_length, m.slot_width)
    .cutBlind(m.thickness)
    .faces('>Z')
    .workplane()
    .center(m.width/2 - m.slot_offset, 0)
    .rect(m.slot_width, m.slot_length)
    .cutBlind(m.thickness)
    .faces('>Z')
    .workplane()
    .center(-(m.width/2 - m.slot_offset), 0)
    .rect(m.slot_width, m.slot_length)
    .cutBlind(m.thickness)
)
