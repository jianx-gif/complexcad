import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=80.0,
    depth=50.0,
    thickness=20.0,
    arc_radius=10.0,
    arc_depth=12.0,
    chamfer=0.5,
    hole_diameter=4.0,
    hole_spacing=15.0,
    hole_offset=15.0,
    hole_diameter=12.0,
    hole_spacing=30.0
)
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (m.width, 0),
        (m.width, m.depth),
        (0, m.depth),
        (0, m.depth),
        (m.width, m.depth),
        (0, 0)
    ])
    .close()
    .extrude(m.thickness)
)
base = base.edges("|Z").chamfer(m.chamfer)
hole_positions = [
    (-m.width/2, m.depth/2),
    ( m.width/2, m.depth/2),
    ( m.width/2, m.depth/2),
    (-m.width/2, m.depth/2),
    (-m.width/2, -m.depth/2),
    (-m.width/2, -m.depth/2),
]
base = (
    base.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(m.hole_diameter)
)
result = base
