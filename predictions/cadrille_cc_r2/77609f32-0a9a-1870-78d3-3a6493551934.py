import cadquery as cq
from types import SimpleNamespace as Measures
measures = Measures(
    width=80.0,
    depth=50.0,
    thickness=8.0,
    rib_height=10.0,
    rib_width=6.0,
    rib_thickness=2.0,
    rib_spacing=15.0,
    rib_spacing=40.0,
    rib_spacing=12.0,
    rib_spacing=15.0,
    rib_spacing=12.0,
    rib_spacing=15.0
)
m = measures
base = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness))
rib = rib.translate((0, 0, m.thickness