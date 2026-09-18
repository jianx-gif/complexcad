import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter = 80.0,
    inner_diameter = 30.0,
    thickness = 6.0,
    rib_height = 4.0,
    rib_width = 10.0,
    rib_depth = 2.0,
    chamfer_distance = 0.5,
    hole_diameter = 5.0,
    hole_depth = 2.0,
    hole_count = 4
)
m.outer_radius = 0.5 * m.outer_diameter
m.outer_radius = m.outer_radius - m.rib_depth
m.outer_radius = m.outer_radius - m.rib_depth
m.outer = (
    cq.Workplane('XY')
    .polyline(m.outer_radius, m.outer_radius)
    .close()
    .revolve()
)
)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(m.rib_width, m.rib_depth)
    .extrude(m.rib_height)
)
result = m.outer.union(rib)
result = (
    result
    .faces('>Z')
    .workplane()
    .center(m.outer_radius - m.rib_depth/2, 0)
    .rect(m.rib_width, m.rib_depth)
    .cutBlind(-m.rib_height)
)
result = (
    result
    .faces('>Z')
    .workplane()
    .center(m.outer_radius - m.rib_depth/2, 0)
    .rect(m.rib_width, m.rib_depth)
    .cutBlind(-m.rib_height)
)
