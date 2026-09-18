import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=30.0,
    depth=5.0,
    thickness=1.0,
    rib_width=12.0,
    rib_height=2.0,
    rib_offset=1.0,
    rib_count=4,
    hole_diameter=5.0,
    hole_offset=15.0,
    hole_spacing=12.0,
    hole_diameter=8.0,
    hole_offset=15.0
)
m.outer_radius = 0.5 * m.outer_radius
m.outer_height = m.depth * m.outer_radius
m.outer_width = m.outer_height - m.depth * m.outer_width
m.outer_depth = m.outer_depth - m.depth * m.outer_width
m.outer = (
    cq.Workplane("XY")
    .moveTo(m.outer_radius, 0)
    .lineTo(m.outer_radius, m.outer_height)
    .lineTo(m.outer_radius + m.outer_width, m.outer_height)
    .lineTo(m.outer_radius + m.outer_width, m.outer_height)
    .lineTo(m.outer_radius, 0)
    .close()
    .revolve(360)
)
m.hole = (
    cq.Workplane("XY")
    .center(m.hole_offset, 0)
    .circle(m.hole_diameter / 2)
    .extrude(m.thickness)
)
result = m.hole(m.hole_diameter)
