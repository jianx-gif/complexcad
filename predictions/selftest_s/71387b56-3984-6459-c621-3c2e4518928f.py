import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    plate_width=80.0,
    plate_depth=30.0,
    plate_thickness=5.0,
    web_width=20.0,
    web_thickness=5.0,
    web_height=12.0,
    hole_diameter=5.0,
    hole_spacing_x=20.0,
    hole_spacing_y=15.0,
    hole_rows=2,
    hole_cols=4,
    chamfer=1.0,
)

base = (
    cq.Workplane("XY")
    .rect(m.plate_width, m.plate_depth)
    .extrude(m.plate_thickness)
)

result = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.web_width, m.web_thickness)
    .extrude(m.web_height)
)

x_start = -((m.hole_cols - 1) * m.hole_spacing_x / 2)
y_start = -((m.hole_rows - 1) * m.hole_spacing_y / 2)
points = [
    (x_start + i * m.hole_spacing_x, y_start + j * m.hole_spacing_y)
    for j in range(m.hole_rows)
    for i in range(m.hole_cols)
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(m.hole_diameter)
)

result = result.edges().chamfer(m.chamfer)
result = result.faces(">Z").edges().chamfer(0.5 * m.chamfer)
