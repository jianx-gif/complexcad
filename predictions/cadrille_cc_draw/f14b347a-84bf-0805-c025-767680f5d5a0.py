import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=80.0,
    depth=50.0,
    thickness=5.0,
    arc_outer_diameter=100.0,
    chamfer=0.5,
    hole_diameter=5.0,
    hole_spacing=15.0,
    hole_offset=15.0,
    hole_count=4,
    hole_spacing=15.0,
    hole_diameter=12.0,
    hole_offset=15.0
)
m.outer_radius = 0.5 * m.outer_diameter
m.outer_depth = m.outer_depth - m.depth
m.outer_radius = m.outer_radius - m.outer_depth
m.outer = (
    cq.Workplane("XY")
    .polyline(m.outer_radius, m.outer_depth)
    .close()
    .extrude(m.depth)
)
m.outer = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(m.outer_radius)
    .extrude(m.depth)
)
result = m.outer.cut(m.outer)
