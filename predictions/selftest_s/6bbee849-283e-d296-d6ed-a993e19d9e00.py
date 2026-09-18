import cadquery as cq
import math
from types import SimpleNamespace as Measures

m = Measures(
    outer_diameter=80.0,
    block_length=60.0,
    thickness=12.0,
    hole_diameter=12.0,
    outer_fillet=2.0,
    inner_fillet=1.0,
    rib_width=10.0,
    rib_depth=8.0,
)

m.outer_radius = m.outer_diameter / 2.0
m.arc_radius = m.outer_radius - m.thickness

result = (
    cq.Workplane('XY')
    .circle(m.outer_radius)
    .workplane(offset=m.block_length)
    .moveTo(-m.arc_radius, 0)
    .threePointArc((0, m.arc_radius), (m.arc_radius, 0))
    .lineTo(-m.arc_radius, 0)
    .close()
    .loft(combine=True)
    .union(
        cq.Workplane('XY')
        .center(m.outer_radius / 2.0, 0)
        .rect(m.rib_width, m.rib_depth)
        .extrude(m.block_length)
    )
    .faces('>Z')
    .workplane()
    .hole(m.hole_diameter)
    .edges('|Z')
    .fillet(m.outer_fillet)
    .edges('>Z')
    .fillet(m.inner_fillet)
)
