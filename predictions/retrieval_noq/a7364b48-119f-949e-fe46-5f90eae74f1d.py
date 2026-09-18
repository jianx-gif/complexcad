import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    outer_width=70.0,
    outer_depth=40.0,
    thickness=8.0,
    slot_width=20.0,
    slot_length=48.0,
    rib_width=8.0,
    rib_height=30.0,
    rib_offset=6.0,
    chamfer=2.0,
    hole=Measures(
        dia=5.0,
        cbore_dia=9.0,
        cbore_depth=3.0,
        offset=12.0
    )
)

base = (
    cq.Workplane('XY')
    .box(m.outer_width, m.outer_depth, m.thickness)
    .edges().chamfer(m.chamfer)
)

slot_cut = (
    base.faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(m.slot_length, m.slot_width)
    .cutBlind(-m.thickness)
)

rib1 = (
    cq.Workplane('XY')
    .center(-m.slot_length/2 - m.rib_offset, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.thickness)
)

rib2 = (
    cq.Workplane('XY')
    .center(m.slot_length/2 + m.rib_offset, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.thickness)
)

combined = slot_cut.union(rib1).union(rib2)

hole_positions = [
    (-m.outer_width/2 + m.hole.offset, 0),
    ( m.outer_width/2 - m.hole.offset, 0)
]

result = (
    combined
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .cboreHole(m.hole.dia, m.hole.cbore_dia, m.hole.cbore_depth)
)
