import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_width=60.0,
    outer_depth=8.0,
    thickness=1.0,
    chamfer=0.5,
    fillet=0.5,
    chamfer=0.5,
    hole_diameter=4.0,
    hole_offset=10.0,
    hole_spacing=12.0,
    hole_diameter=6.0,
    hole_offset=15.0
)
m.outer = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(m.outer_width, 0)
    .lineTo(m.outer_width, m.outer_depth)
    .lineTo(m.outer_width, m.outer_depth)
    .lineTo(m.outer_width, m.outer_depth)
    .lineTo(m.outer_width, 0)
    .close()
    .extrude(m.thickness)
)
result = (
    m.outer
    .faces(">Z")
    .workplane()
    .center(m.outer_width/2, m.outer_depth/2)
    .hole(m.hole_diameter)
    .edges("|Z")
    .chamfer(m.chamfer)
)
