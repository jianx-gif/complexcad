import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    width=30.0,
    depth=20.0,
    thickness=6.0,
    slot_width=10.0,
    slot_depth=18.0,
    tab_length=8.0,
    corner_fillet=1.5,
    hole_diameter=3.0,
    hole_spacing=12.0,
    rib_width=4.0,
    rib_height=4.0
)

# Base spacer
base = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
)

# Central slot pocket (half depth)
slot = (
    base
    .faces(">Z")
    .workplane()
    .rect(m.slot_width, m.slot_depth)
    .cutBlind(-m.thickness/2)
)

# Add internal rib on bottom face
rib = (
    slot
    .faces("<Z")
    .workplane()
    .rect(m.rib_width, m.rib_height)
    .extrude(m.thickness/4)
)

# Extrude tab on +X side
with_tab = (
    rib
    .faces(">X")
    .workplane()
    .rect(m.thickness, m.depth)
    .extrude(m.tab_length)
)

# Top holes pattern
with_holes = (
    with_tab
    .faces(">Z")
    .workplane()
    .pushPoints([(-m.hole_spacing/2, 0), (m.hole_spacing/2, 0)])
    .hole(m.hole_diameter)
)

# Fillet top outer corner (positive Y, positive Z)
result = (
    with_holes
    .edges("|Y").edges(">Z")
    .fillet(m.corner_fillet)
)
