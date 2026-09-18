import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter = 80.0,
    height = 60.0,
    wall_thickness = 4.0,
    rib_height = 12.0,
    rib_width = 12.0,
    rib_thickness = 5.0,
    rib_height = 15.0,
    chamfer_distance = 0.5,
    hole_diameter = 4.0,
    hole_spacing = 12.0,
    hole_offset = 15.0,
)
m.outer_radius = 0.5 * m.outer_diameter
m.inner_radius = m.outer_radius - m.outer_diameter
m.inner_radius = m.inner_radius - m.inner_radius
m.inner_radius = m.inner_radius - m.inner_radius
m.inner_radius = m.inner_radius - m.inner_radius
m.inner_radius = m.inner_radius - m.inner_radius
m.inner_radius = m.inner_radius - m.inner_radius
m.inner = (
    cq.Workplane("XY")
    .circle(m.inner_radius)
    .extrude(m.height)
    .faces(">Z")
    .workplane()
    .circle(m.inner_radius)
    .cutBlind(m.height)
)
rib = (
    cq.Workplane("XY")
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
    .translate((0, 0, m.height))
)
rib = rib.union(rib)
hole_positions = [
    ( m.inner_radius * m.hole_spacing, m.inner_radius * m.hole_spacing),
    (-m.inner_radius * m.hole_spacing, m.inner_radius * m.hole_spacing),
    ( m.inner_radius * m.hole_spacing, m.inner_radius * m.hole_spacing),
    (-m.inner_radius * m.inner_radius, m.inner_radius * m.inner_radius),
]
result = (
    rib
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(m.hole_diameter)
)
