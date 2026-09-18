import cadquery as cq
from types import SimpleNamespace as Measures

p = Measures(
    width = 60.0,
    height = 30.0,
    thickness = 8.0,
    rib_height = 12.0,
    rib_thickness = 4.0,
    slot_width = 6.0,
    slot_length = 45.0,
    relief_width = 8.0,
    relief_depth = 4.0,
    counterbore_dia = 8.0,
    counterbore_depth = 3.0,
    counterbore_large_dia = 12.0,
    chamfer = 0.5,
    clearance = 2.0
)

base = (
    cq.Workplane('XY')
    .rect(p.width, p.height)
    .polygon(3, p.rib_thickness)
    .translate((0, p.height/4))
    .extrude(p.thickness)
)

slot_cut = (
    base
    .faces('>Z')
    .workplane()
    .rect(p.slot_length, p.slot_width)
    .cutBlind(-p.thickness)
)

relief_cut = (
    slot_cut
    .faces('>X')
    .workplane()
    .rect(p.relief_width, p.height - 2 * p.clearance)
    .cutBlind(-p.relief_depth)
)

counterbore_cut = (
    relief_cut
    .faces('>Z')
    .workplane()
    .hole(p.counterbore_dia)
    .hole(p.counterbore_large_dia, depth=p.counterbore_depth)
)

result = (
    counterbore_cut
    .faces('>Z')
    .edges()
    .chamfer(p.chamfer)
)
