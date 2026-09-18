import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_width=60.0,
    outer_depth=20.0,
    thickness=5.0,
    wall_thickness=2.0,
    chamfer=0.5,
    hole_diameter=4.0,
    hole_depth=12.0,
    hole_offset=15.0,
    hole_diameter=10.0,
    hole_spacing=30.0,
    hole_offset=15.0
)
base = (
    cq.Workplane("XY")
    .box(m.outer_width, m.outer_depth, m.thickness)
    .translate((0, 0, m.thickness / 2))
)
base = (
    base.faces(">Z").workplane()
    .rect(m.outer_width - 2 * m.wall_thickness, m.wall_depth)
    .cutBlind(-m.wall_thickness)
)
base = (
    base.faces(">Z").workplane()
    .rect(m.wall_thickness, m.wall_depth)
    .extrude(m.wall_thickness)
)
base = base.edges("|Z").chamfer(m.chamfer)
result = base
