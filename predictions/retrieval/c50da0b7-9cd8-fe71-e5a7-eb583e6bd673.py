import cadquery as cq
from types import SimpleNamespace as Measures

params = Measures(
    total_length=80.0,
    shank_radius=4.0,
    shank_length=55.0,
    head_radius=8.0,
    head_height=10.0,
    head_chamfer=1.0,
    turn_hole_diameter=5.0,
    knurl_length=12.0,
    knurl_tooth_width=1.5,
    knurl_tooth_height=2.0,
    knurl_tooth_depth=1.0,
    knurl_count=20,
    base_chamfer=0.8
)

p = params

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(p.shank_radius, 0)
    .vLine(p.shank_length)
    .lineTo(p.head_radius, p.shank_length)
    .vLine(p.head_height)
    .close()
)

pin_body = profile.revolve()

pin_body = (
    pin_body
    .faces(">Z").chamfer(p.head_chamfer)
    .faces("<Z").chamfer(p.base_chamfer)
)

pin_body = (
    pin_body
    .faces("<Z").workplane()
    .hole(p.turn_hole_diameter)
)

# Knurl tooth geometry
tooth = (
    cq.Workplane("XY")
    .box(p.knurl_tooth_width, p.knurl_tooth_depth, p.knurl_tooth_height)
    .translate((p.shank_radius + p.knurl_tooth_depth/2, 0, 0))
)

knurl_start_z = p.shank_length + p.head_height - p.knurl_length

knurl = (
    tooth
    .translate((0, 0, knurl_start_z + p.knurl_length/2))
    .polarArray(count=p.knurl_count, radius=0, startAngle=0, angle=360)
)

# Combine solids via a new workplane
result = cq.Workplane().add(pin_body).add(knurl).combine()
