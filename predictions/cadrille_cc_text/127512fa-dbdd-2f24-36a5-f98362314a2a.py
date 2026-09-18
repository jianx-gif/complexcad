import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=80.0,
    height=60.0,
    thickness=8.0,
    flange_width=20.0,
    flange_height=20.0,
    flange_width=30.0,
    slot_length=30.0,
    slot_width=10.0,
    slot_width=10.0,
    flange_height=20.0,
    fillet_radius=1.5,
    fillet_radius=2.0,
)
base = (
    cq.Workplane("XY")
    .rect(m.width, m.height)
    .extrude(m.thickness)
)
base = base.edges("|Z").fillet(m.fillet_radius)
base = base.edges("|Z").chamfer(m.fillet_radius)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.slot_width, m.slot_height)
    .cutBlind(-m.thickness)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .hole(m.mount_hole_dia)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .hole(m.mount_hole_dia)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.slot_width, m.slot_height)
    .extrude(m.flange_width)
)
base = base.edges("|Z").fillet(m.fillet_radius)
result = base
