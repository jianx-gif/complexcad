import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    outer_diameter=40.0,
    body_height=12.0,
    hole_diameter=12.0,
    groove_diameter=28.0,
    groove_width=2.0,
    groove_depth=1.5,
    chamfer_size=0.5,
    flange_width=20.0,
    flange_height=6.0,
    flange_thickness=4.0,
    notch_width=6.0,
    notch_height=3.0
)

# Main cylindrical spacer
result = (
    cq.Workplane("XY")
    .circle(m.outer_diameter / 2)
    .extrude(m.body_height)
    .hole(m.hole_diameter)
)

# Snap ring groove cutter
groove_z = m.body_height * 0.55
groove_cutter = (
    cq.Workplane("XY")
    .circle(m.groove_diameter / 2 + m.groove_depth)
    .circle(m.groove_diameter / 2)
    .extrude(m.groove_width)
    .translate((0, 0, groove_z - m.groove_width / 2))
)
result = result.cut(groove_cutter)

# Chamfer base edge
result = result.edges("<Z").chamfer(m.chamfer_size)

# Composite side flange with a triangular protrusion (non‑trivial sketch)
flange_sketch = (
    cq.Workplane("XY")
    .sketch()
    .rect(m.flange_width, m.flange_height)
    .polygon([
        (-m.notch_width/2, m.flange_height/2),
        ( m.notch_width/2, m.flange_height/2),
        (0, m.flange_height/2 + m.notch_height)
    ])
    .finalize()
    .extrude(m.flange_thickness)
)
flange_position = (
    m.outer_diameter / 2 + m.flange_thickness / 2,
    0,
    m.body_height - m.flange_height / 2
)
flange = flange_sketch.translate(flange_position)
result = result.union(flange)
