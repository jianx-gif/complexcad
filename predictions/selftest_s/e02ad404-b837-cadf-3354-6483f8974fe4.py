import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    inner_radius=30.0,
    outer_radius=40.0,
    tab_width=12.0,
    height=30.0,
    tab_height=8.0,
    flex_cut_depth=2.0,
    flex_cut_thickness=2.0,
    hole_diameter=3.0,
    hole_spacing=8.0,
    hole_count=3,
    chamfer=1.0,
)

base = (
    cq.Workplane("XZ")
    .moveTo(m.inner_radius, 0)
    .lineTo(m.inner_radius, m.height - m.tab_height)
    .lineTo(m.outer_radius, m.height - m.tab_height)
    .lineTo(m.outer_radius + m.tab_width, m.height - m.tab_height)
    .lineTo(m.outer_radius + m.tab_width, m.height)
    .lineTo(m.outer_radius, m.height)
    .lineTo(m.inner_radius, m.height)
    .close()
    .revolve(360)
)

model = (
    base.edges()
    .chamfer(m.chamfer)
)

model = (
    model.faces(">Z").workplane()
    .center(m.outer_radius + m.tab_width/2, 0)
    .rect(m.tab_width, m.flex_cut_thickness)
    .cutBlind(m.flex_cut_depth)
)

hole_positions = []
start = -((m.hole_count - 1) * m.hole_spacing) / 2
for i in range(m.hole_count):
    hole_positions.append((start + i * m.hole_spacing, 0))

result = (
    model.faces(">Z").workplane()
    .center(m.outer_radius + m.tab_width/2, 0)
    .pushPoints(hole_positions)
    .hole(m.hole_diameter)
)
