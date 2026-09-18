import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_width=60.0,
    outer_depth=80.0,
    wall_thickness=8.0,
    wall_thickness=2.0,
    chamfer=0.5,
    hole_diameter=5.0,
    hole_offset=15.0,
    chamfer=0.5
)
m.outer_radius = m.outer_radius + m.wall_thickness
m.outer_depth = m.outer_depth - m.wall_thickness
m.outer_radius = m.outer_radius - m.wall_thickness
m.outer = (
    cq.Workplane("XY")
    .polyline(m.outer_radius, m.outer_radius)
    .close()
    .extrude(m.outer_depth)
)
result = (
    m.outer
    .faces(">Z")
    .workplane()
    .center(0, m.outer_radius - m.wall_thickness/2)
    .rect(m.slot_thickness, m.slot_depth)
    .cutBlind(-m.wall_thickness)
    .edges("|Z")
    .chamfer(m.chamfer)
)
