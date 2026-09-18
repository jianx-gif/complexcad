import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=70.0,
    depth=30.0,
    thickness=3.0,
    wall=1.5,
    rib_width=10.0,
    rib_height=2.0,
    rib_spacing=12.0,
    rib_count=4,
    hole_diameter=5.0,
    hole_offset_x=15.0,
    hole_offset_y=10.0,
    hole_diameter=8.0,
    hole_offset_x=15.0
)
base = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(m.rib_width, m.depth)
    .extrude(m.rib_height)
)
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.rib_width/2, 0, m.rib_count))
rib = rib.translate((m.width/2 - m.