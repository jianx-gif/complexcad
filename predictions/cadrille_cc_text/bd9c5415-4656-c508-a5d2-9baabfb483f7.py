import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=30.0,
    depth=20.0,
    thickness=6.0,
    corner_fillet=1.5,
    slot_width=10.0,
    slot_depth=18.0,
    rib_height=4.0,
    rib_width=4.0,
    hole_diameter=3.0,
    hole_spacing=12.0,
    hole_rows=2,
    hole_cols=3,
    hole_rows=4,
    hole_cols=4,
    hole_spacing=12.0,
)
base = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
)
base = base.edges().fillet(m corner_fillet)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.slot_width, m.slot_depth)
    .cutBlind(-m.thickness)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.slot_width, m.slot_depth)
    .cutBlind(-m.thickness)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_width)
)
base = base.edges("|Z").fillet(m.fillet)
base = (
    base.faces(">Z").workplane()
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter)
)
base = (
    base.faces(">Z").workplane()
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter)
)
result = base
