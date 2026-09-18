import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    thickness=10.0,
    width=12.0,
    thickness=15.0,
    fillet_radius=2.0,
    gusset_thickness=5.0,
    gusset_thickness=5.0,
    counterbore_dia=8.0,
    counterbore_depth=3.0,
    clearance_dia=6.0,
    clearance_count=4,
    hole_dia=4.0,
    hole_spacing=20.0
)
m.arc_center_radius = m.thickness / 2.0
m.arc_center_angle = math.degrees(math.acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180.0 - m.arc_center_angle)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)
base = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.width, m.thickness)
    .extrude(m.thickness)
)
base = base.union(m.base)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(m.clearance_dia, m.clearance_count, m.clearance_count, m.clearance_count)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(m.clearance_dia, m.clearance_count, m.clearance_count)
)
result = (
    base
    .edges("|Z")
    .fillet(m.fillet_radius)
)
