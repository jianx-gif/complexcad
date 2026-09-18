import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_width=70.0,
    outer_height=30.0,
    thickness=10.0,
    wall_thickness=2.0,
    rib_width=12.0,
    rib_height=5.0,
    rib_offset=15.0,
    hole_diameter=4.0,
    hole_spacing=15.0,
    hole_offset=12.0,
    hole_diameter=6.0,
    hole_spacing=15.0
)
m.outer_radius = 0.5 * m.outer_radius
m.outer_depth = m.outer_depth - m.rib_height
m.outer_radius = m.outer_radius - m.rib_width
m.outer = (
    cq.Workplane("XY")
    .polyline(m.outer_radius, m.outer_radius)
    .lineTo(m.outer_radius, m.outer_radius)
    .lineTo(m.outer_radius, m.outer_height)
    .lineTo(m.outer_radius, m.outer_height)
    .lineTo(m.outer_radius, m.outer_height + m.rib_height)
    .lineTo(m.outer_radius, m.outer_height + m.rib_height)
    .lineTo(m.outer_radius, m.outer_height + m.rib_height)
    .lineTo(m.outer_radius, m.outer_height)
    .lineTo(m.outer_radius, 0)
    .lineTo(m.outer_radius, 0)
    .close()
)
result = (
    m.outer
    .extrude(m.rib_height)
    .edges("|Z")
    .chamfer(m.chamfer)
    .faces(">Z")
    .workplane()
    .center(m.outer_radius - m.rib_offset, m.rib_height/2)
    .rarray(m.hole_spacing, 0, m.hole_spacing, 1)
    .hole(m.hole_diameter)
)
