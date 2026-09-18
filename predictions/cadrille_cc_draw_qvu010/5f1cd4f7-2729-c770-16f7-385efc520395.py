import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=40.0,
    depth=10.0,
    thickness=12.0,
    rib_width=12.0,
    rib_height=10.0,
    rib_thickness=5.0,
    rib_spacing=12.0,
    rib_count=4,
    hole_diameter=5.0,
    hole_spacing=15.0,
    hole_diameter=8.0,
    hole_offset_x=20.0,
    hole_offset_y=10.0
)
m.outer_radius = 0.5 * m.outer_radius
m.outer_height = m.outer_height - m.depth
m.outer = (
    cq.Workplane("XY")
    .moveTo(m.outer_radius, 0)
    .lineTo(m.outer_radius, m.outer_height)
    .lineTo(m.outer_radius, m.outer_height)
    .lineTo(m.outer_radius, m.outer_height + m.depth)
    .lineTo(m.outer_radius, m.outer_height + m.depth)
    .lineTo(m.outer_radius, 0)
    .close()
    .revolve(360)
)
m.hole = (
    cq.Workplane("XY")
    .center(m.hole_offset_x, 0)
    .circle(m.hole_diameter / 2)
    .extrude(m.thickness)
)
result = m.hole.mirror(m.top_radius)
