import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    base_width=60.0,
    base_height=40.0,
    spacer_thickness=8.0,
    diagonal_offset=10.0,
    hole_diameter=12.0,
    relief_width=8.0,
    relief_height=12.0,
    chamfer_size=2.0,
    rib_thickness=2.0
)

points = [
    (0, 0),
    (m.base_width, 0),
    (m.base_width, m.diagonal_offset),
    (m.base_width - m.diagonal_offset, m.diagonal_offset),
    (m.base_width - m.diagonal_offset, m.base_height),
    (0, m.base_height)
]

base = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(m.spacer_thickness)
)

rib = (
    cq.Workplane("XY")
    .center(m.base_width/2 - m.diagonal_offset/2, m.base_height/2)
    .rect(m.base_width/4, m.base_height/4)
    .extrude(m.rib_thickness)
)

result = (
    base.union(rib)
    .faces(">Z").edges().chamfer(m.chamfer_size)
    .faces(">Z").workplane()
    .hole(m.hole_diameter)
    .faces(">X").workplane(centerOption='CenterOfMass')
    .rect(m.relief_width, m.relief_height)
    .cutBlind(-m.spacer_thickness/2)
    .faces("<X").workplane(centerOption='CenterOfMass')
    .rect(m.relief_width, m.relief_height)
    .cutBlind(-m.spacer_thickness/2)
)
