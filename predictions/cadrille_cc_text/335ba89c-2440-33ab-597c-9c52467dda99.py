import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=30.0,
    width=5.0,
    inner_fillet=2.0,
    relief_width=15.0,
    relief_depth=20.0,
    relief_height=3.0,
    hole_diameter=5.0,
    hole_cbore_diameter=7.5,
    hole_cbore_depth=2.0,
    hole_spacing_x=30.0,
    hole_spacing_y=30.0,
    holes_offset_x=20.0,
    holes_offset_y=30.0,
    chamfer=1.0
)
base = (
    cq.Workplane("XY")
    .rect(m.width, m.thickness)
    .extrude(m.thickness)
)
base = base.edges("|Z").fillet(m.inner_fillet)
base = base.edges(">Z").chamfer(m.chamfer)
hole_positions = [
    (m.hole_spacing_x/2, m.hole_spacing_y/2),
    (-m.hole_spacing_x/2, m.hole_spacing_y/2),
    ( m.hole_spacing_x/2, m.hole_spacing_y/2),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cboreHole(m.hole_diameter, m.hole_cbore_diameter, m.hole_cbore_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(m.relief_width, m.relief_depth)
    .cutBlind(-m.relief_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(m.relief_width/2, m.relief_depth/2)
    .rect(m.relief_width, m.relief_depth)
    .cutBlind(-m.relief_depth)
)
result = base
