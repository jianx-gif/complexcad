import cadquery as cq
import math
from types import SimpleNamespace as Measures

m = Measures(
    outer_radius=40.0,
    inner_radius=30.0,
    axial_height=10.0,
    split_gap_angle=12.0,
    inner_fillet_radius=1.5,
    inner_chamfer=0.8,
    outer_notch_width=4.0,
)

half_height = m.axial_height / 2.0
gap_width = 2 * m.outer_radius * math.tan(math.radians(m.split_gap_angle / 2.0))

base = (
    cq.Workplane("XY")
    .polyline([
        (m.inner_radius, -half_height),
        (m.outer_radius, -half_height),
        (m.outer_radius, half_height),
        (m.inner_radius, half_height),
        (m.inner_radius, -half_height)
    ])
    .close()
    .revolve()
)

ring = base.edges().fillet(m.inner_fillet_radius)

split_cut = (
    cq.Workplane("XY")
    .box(gap_width, m.axial_height * 2.0, m.outer_radius * 2.0)
    .edges().chamfer(m.inner_chamfer)
    .translate((0, m.outer_radius + gap_width / 2.0, 0))
)
ring = ring.cut(split_cut)

outer_notch = (
    cq.Workplane("XY")
    .rect(m.outer_notch_width, m.outer_radius * 2.0)
    .extrude(m.axial_height * 2.0)
    .translate((m.outer_radius / 2.0, 0, -half_height))
)
ring = ring.cut(outer_notch)

result = ring