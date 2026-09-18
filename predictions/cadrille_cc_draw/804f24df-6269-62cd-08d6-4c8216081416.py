import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_radius = 30.0,
    inner_radius = 20.0,
    thickness = 10.0,
    rib_width = 12.0,
    rib_height = 8.0,
    rib_thickness = 5.0,
    rib_offset = 15.0,
    chamfer_distance = 0.5,
    hole_diameter = 5.0,
    hole_spacing = 12.0,
    hole_offset = 15.0,
    hole_count = 4
)
m.outer_radius = 0.5 * m.outer_radius
m.outer = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (m.outer_radius, 0),
        (m.outer_radius, m.outer_radius),
        (0, m.outer_radius),
    ])
    .close()
    .extrude(m.thickness)
)
m.outer = (
    cq.Workplane("XY")
    .polyline([
        (0, m.outer_radius),
        (m.outer_radius, m.outer_radius),
        (m.outer_radius, m.outer_radius - m.rib_offset),
        (0, m.outer_radius - m.rib_offset),
        (0, m.outer_radius)
    ])
    .close()
    .extrude(m.thickness)
)
result = (
    m.outer
    .faces(">Z")
    .workplane()
    .pushPoints([
        (m.inner_radius, m.inner_radius),
        (m.inner_radius, m.inner_radius),
        (0, m.inner_radius)
    ])
    .hole(m.hole_diameter)
)
