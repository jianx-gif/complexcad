import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=60.0,
    depth=15.0,
    thickness=4.0,
    wall=1.5,
    rib_width=10.0,
    rib_height=2.0,
    rib_offset=10.0,
    rib_count=4,
    hole_diameter=5.0,
    hole_spacing=12.0,
    hole_offset=10.0
)
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (m.width, 0),
        (m.width, m.depth),
        (m.width - m.depth, m.depth),
        (m.width - m.depth, m.depth),
        (m.width - m.depth, m.depth),
        (0, m.depth),
        (0, 0)
    ])
    .close()
    .extrude(m.thickness)
)
base = base.edges("|Z").chamfer(m.chamfer)
rib = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, m.depth)
    .extrude(m.rib_height)
)
rib = rib.faces(">Z").edges().chamfer(m.chamfer)
result = rib
