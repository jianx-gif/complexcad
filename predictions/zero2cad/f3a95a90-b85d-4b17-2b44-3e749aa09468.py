import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    base_width=80.0,
    base_depth=30.0,
    base_thickness=6.0,
    tab_width=30.0,
    tab_depth=15.0,
    tab_height=5.0,
    fillet_radius=2.0,
    hole_diameter=3.0,
    countersink_diameter=5.5,
    countersink_angle=82.0,
    hole_spacing=20.0,
    hole_count=2
)

base = (
    cq.Workplane("XY")
    .box(m.base_width, m.base_depth, m.base_thickness)
    .translate((0, 0, m.base_thickness / 2))
)

tab = (
    cq.Workplane("XY")
    .workplane(offset=m.base_thickness)
    .rect(m.tab_width, m.tab_depth)
    .extrude(m.tab_height)
)

combined = base.union(tab)

combined = combined.faces(">Z").edges().fillet(m.fillet_radius)

hole_positions = [(-m.hole_spacing/2, 0), (m.hole_spacing/2, 0)]

result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(m.hole_diameter, m.countersink_diameter, m.countersink_angle, m.tab_height)
)
