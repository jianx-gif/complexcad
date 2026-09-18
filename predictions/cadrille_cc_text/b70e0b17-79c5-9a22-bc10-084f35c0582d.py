import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=60.0,
    depth=12.0,
    height=20.0,
    arc_outer_diameter=80.0,
    slot_width=30.0,
    slot_height=12.0,
    rib_width=25.0,
    rib_height=10.0,
    rib_thickness=4.0,
    arc_outer_radius=20.0,
    edge_chamfer=0.5
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = math.degrees(math.atan(2 * math.pi * m.arc_center_angle))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path, transition="round")
    .edges("|Z")
    .chamfer(m.edge_chamfer)
    .faces(">Z")
    .workplane()
    .center(m.arc_center_radius, 0)
    .rect(m.depth, m.height)
    .cutBlind(m.depth)
    .faces(">Z")
    .workplane()
    .center(m.arc_center_radius, 0)
    .rect(m.depth, m.height)
    .cutBlind(m.depth)
    .faces(">Z")
    .workplane()
    .center(m.arc_center_radius, 0)
    .rect(m.depth, m.height)
    .cutBlind(m.depth)
)
