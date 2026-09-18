import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter = 80.0,
    inner_diameter = 30.0,
    thickness = 10.0,
    chamfer_distance = 1.0,
    slot_width = 6.0,
    slot_height = 4.0,
    slot_offset = 15.0,
    slot_offset = 10.0
)
m.outer_radius = 0.5 * m.outer_diameter
m.outer_depth = m.outer_radius - m.rib_thickness
m.outer_radius = m.outer_radius - m.rib_thickness
m.outer = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(m.outer_radius, 0)
    .lineTo(m.outer_radius, m.outer_depth)
    .lineTo(m.outer_radius + m.outer_depth, m.outer_depth)
    .lineTo(m.outer_radius + m.outer_depth, m.outer_depth)
    .lineTo(m.outer_radius + m.outer_depth, m.outer_depth)
    .lineTo(m.outer_radius, m.outer_depth)
    .close()
)
result = (
    cq.Workplane("XY")
    .center(m.outer_radius - m.outer_radius, m.outer_depth / 2)
    .rect(m.outer_radius * m.outer_radius, m.outer_depth)
    .extrude(m.outer_depth)
    .edges("|Z")
    .chamfer(m.chamfer_distance)
    .faces(">Z")
    .workplane()
    .center(m.outer_radius - m.inner_radius - m.inner_depth / 2, m.inner_depth / 2)
    .rect(m.inner_radius * m.inner_radius, m.inner_depth)
    .cutBlind(-m.inner_depth)
    .edges(">Z")
    .chamfer(m.chamfer_distance)
)
