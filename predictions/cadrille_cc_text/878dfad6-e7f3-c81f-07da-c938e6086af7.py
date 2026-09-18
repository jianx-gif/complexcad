import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=60.0,
    height=30.0,
    thickness=8.0,
    wall=3.0,
    rib_height=12.0,
    rib_thickness=4.0,
    relief_width=6.0,
    relief_depth=4.0,
    counterbore_dia=8.0,
    counterbore_large_dia=12.0,
    counterbore_large_dia=12.0,
    chamfer=0.5,
    hole=Measures(
        diameter=Measures(
        diameter=Measures(
        position=Measures(
        position=Measures(
        position=Measures()
    )
)
result = (
    cq.Workplane("XY")
    .rect(m.width, m.height)
    .extrude(m.thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .polygon(6, m.depth)
    .cutBlind(-m.thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .polygon(6, m.depth)
    .cutBlind(-m.thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(m.counterbore_dia)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(m.counterbore_dia)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(m.counterbore_dia)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(m.counterbore_dia)
)
