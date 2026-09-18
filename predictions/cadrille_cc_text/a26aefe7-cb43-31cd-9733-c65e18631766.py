import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=60.0,
    depth=30.0,
    height=8.0,
    tab_length=15.0,
    tab_width=20.0,
    tab_thickness=2.0,
    snap_gap=2.0,
    hole_diameter=4.0,
    hole_depth=5.0,
    hole_count=4,
)
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (m.width, 0),
        (m.width, m.depth),
        (m.depth, m.depth),
        (m.depth, m.depth),
        (m.depth, m.height),
        (0, m.height),
        (0, 0)
    ])
    .close()
    .extrude(m.depth)
)
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([
        (m.width/2, m.depth/2),
        (m.width/2, m.depth/2),
        (m.depth/2, m.depth/2)
    ])
    .hole(m.hole_diameter)
    .faces(">Z")
    .workplane()
    .pushPoints([(-m.hole_count/2, 0), (m.hole_count/2, 0)])
    .hole(m.hole_diameter)
    .faces(">Z")
    .workplane()
    .pushPoints([(-m.hole_count/2, 0), (m.hole_count/2, 0)])
    .hole(m.hole_diameter)
)
