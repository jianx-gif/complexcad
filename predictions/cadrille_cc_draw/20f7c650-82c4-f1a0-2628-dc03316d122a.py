import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    plate_width=70.0,
    plate_depth=30.0,
    thickness=5.0,
    tab_width=12.0,
    tab_height=15.0,
    tab_thickness=5.0,
    hole_diameter=6.0,
    hole_spacing=15.0,
    hole_offset=15.0,
    chamfer=0.5,
)
m.outer_radius = 0.5 * m.outer_radius
m.outer_depth = m.outer_depth - m.plate_thickness
m.outer_radius = m.outer_radius - m.plate_thickness
m.outer = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (m.outer_radius, 0),
        (m.outer_radius, m.outer_depth),
        (m.outer_radius, m.outer_depth),
        (0, m.outer_depth),
        (0, 0)
    ])
    .close()
    .extrude(m.thickness)
)
result = (
    cq.Workplane("XY")
    .center(m.outer_radius - m.thickness/2, 0)
    .circle(m.hole_diameter/2)
    .extrude(m.thickness)
    .edges("|Z")
    .chamfer(m.chamfer)
)
