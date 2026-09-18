import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter=80.0,
    height=12.0,
    arc_outer_diameter=80.0,
    top_fillet=2.0,
    chamfer=0.5,
    hole_diameter=4.0,
    hole_spacing=15.0,
    hole_offset=10.0,
    hole_offset=20.0,
    hole_diameter=4.0,
    hole_spacing=15.0,
    hole_spacing=12.0,
    hole_offset=15.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.linear_fillet**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_fillet, m.arc_center_diameter/2), m.arc_center_radius)
    .wire()
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path)
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path)
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path)
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path)
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path)
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.slot_fillet, m.slot_fillet)
    .sweep(path)
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.slot_fillet/2, 0))
    .rect(m.slot_fillet, m.slot_fillet)
    .sweep(path)
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.slot_fillet/2, 0))
    .rect(m.slot_diameter, m.slot_diameter)
    .sweep(path)
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.slot_fillet/2, 0))
    .rect(m.slot_diameter, m.slot_diameter)
    .sweep(path)
)
path = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.slot_fillet/2, 0))
    .rect(m.slot_diameter, m.slot_diameter)
    .extrude(m.slot_fillet)
)
path = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, m.height/2))
    .rect(m.slot_diameter, m.slot_diameter)
    .extrude(m.slot_fillet)
)
result = path.cut(m.slot)
