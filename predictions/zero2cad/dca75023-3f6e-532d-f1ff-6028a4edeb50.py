import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    width=60.0,
    depth=40.0,
    thickness=12.0,
    central_hole_dia=15.0,
    central_hole_depth=6.0,
    side_slot_width=8.0,
    side_slot_depth=6.0,
    side_slot_offset=10.0,
    chamfer=1.0,
    mount_hole_dia=6.0,
    mount_hole_spacing=30.0,
    mount_hole_offset=5.0
)

result = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
    .faces("<Z")
    .workplane()
    .hole(m.central_hole_dia, depth=m.central_hole_depth)
    .faces(">Z")
    .workplane()
    .hole(m.mount_hole_dia)
    .faces(">Z")
    .workplane()
    .pushPoints([(-m.mount_hole_spacing/2, 0), (m.mount_hole_spacing/2, 0)])
    .hole(m.mount_hole_dia)
    .faces("<X")
    .workplane()
    .center(0, m.side_slot_offset)
    .rect(m.side_slot_width, m.side_slot_depth)
    .cutBlind(-m.thickness/2)
    .edges("|Z")
    .chamfer(m.chamfer)
)
