import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=80.0,
    depth=30.0,
    height=12.0,
    arc_outer_diameter=40.0,
    arc_outer_diameter=60.0,
    hole_diameter=4.0,
    hole_spacing=15.0,
    hole_offset=10.0,
    hole_diameter=4.0,
    hole_depth=3.0,
    hole_offset=15.0
)
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_radius = 0.5 * m.arc_outer_diameter
m.arc_center_angle = degrees(acos((2 * m.arc_center_radius**2 - m.arc_center_angle), m.arc_center_radius**2 - m.arc_center_angle)
arc_path = (
    cq.Workplane("XY")
    .radiusArc((m.arc_center_radius, 0), m.arc_center_radius)
    .wire()
)
base = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_center_angle, 0))
    .rect(m.depth, m.height)
    .sweep(arc_path, transition="round")
)
base = base.edges("|Z").fillet(m.top_fillet)
base = base.edges(">Z").fillet(m.top_fillet)
base = base.faces(">Z").edges().chamfer(m.chamfer)
base = (
    base.faces(">Z").workplane()
    .pushPoints([(-m.hole_offset, 0), (m.hole_offset, 0)])
    .hole(m.hole_diameter)
)
base = (
    base.faces(">Z").workplane()
    .pushPoints([(-m.hole_offset, 0), (m.hole_offset, 0)])
    .hole(m.hole_diameter)
)
result = base
