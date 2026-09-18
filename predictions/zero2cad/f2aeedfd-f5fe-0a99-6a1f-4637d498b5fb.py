import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    length=80.0,
    width=20.0,
    thickness=8.0,
    fillet_radius=2.0,
    slot_length=30.0,
    slot_width=6.0,
    slot_offset=10.0,
    hole1=Measures(
        position=15.0,
        diameter=5.0,
        cbore_diameter=8.0,
        cbore_depth=2.0
    ),
    hole2=Measures(
        position=65.0,
        diameter=5.0,
        cbore_diameter=8.0,
        cbore_depth=2.0
    )
)

result = (
    cq.Workplane("XY")
    .box(m.length, m.width, m.thickness)
    .translate((0.5 * m.length, 0, 0.5 * m.thickness))
    .faces(">X").edges().fillet(m.fillet_radius)
    .faces(">Y").workplane()
    .center(m.slot_offset + 0.5 * m.slot_length, 0)
    .rect(m.slot_length, m.slot_width)
    .cutBlind(-m.thickness)
    .faces("<Z").workplane()
    .pushPoints([(m.hole1.position, 0), (m.hole2.position, 0)])
    .cboreHole(m.hole1.diameter, m.hole1.cbore_diameter, m.hole1.cbore_depth)
)
