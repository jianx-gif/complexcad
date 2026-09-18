import cadquery as cq
from types import SimpleNamespace as NS

m = NS(
    width=60.0,
    depth=30.0,
    height=8.0,
    tab_length=15.0,
    tab_extension=10.0,
    snap_gap=2.0,
    snap_depth=6.0,
    hole_diameter=4.0,
    hole_depth=5.0,
    hole_offsets=[15.0, 30.0, 45.0]
)

base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (m.width, 0),
        (m.width, m.depth),
        (m.width + m.tab_length, m.depth),
        (m.width + m.tab_length, m.depth + m.tab_extension),
        (m.width, m.depth + m.tab_extension),
        (0, m.depth),
        (0, 0)
    ]).close()
    .extrude(m.height)
)

bracket = (
    base
    .faces(">Y")
    .workplane()
    .center(m.width/2, m.depth + m.tab_extension/2)
    .rect(m.tab_length, m.snap_gap)
    .cutBlind(m.snap_depth)
)

result = (
    bracket
    .faces(">Z")
    .workplane()
    .pushPoints([(p, m.depth/2) for p in m.hole_offsets])
    .hole(m.hole_diameter, depth=m.hole_depth)
)
