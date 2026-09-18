import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    total_length=80.0,
    shaft_diameter=8.0,
    head_diameter=16.0,
    head_height=12.0,
    knurl_depth=0.8,
    knurl_width=1.2,
    knurl_count=12,
    set_screw_diameter=3.0,
    set_screw_cbore_diameter=6.0,
    set_screw_cbore_depth=4.0,
    chamfer=0.5
)

shaft_radius = m.shaft_diameter / 2.0
head_radius = m.head_diameter / 2.0
shaft_length = m.total_length - m.head_height

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(shaft_radius, 0)
    .lineTo(shaft_radius, shaft_length)
    .lineTo(head_radius, shaft_length)
    .lineTo(head_radius, m.total_length)
    .lineTo(0, m.total_length)
    .close()
)

pin = profile.revolve()

pin = (
    pin
    .faces(">Z")
    .workplane()
    .cboreHole(m.set_screw_diameter, m.set_screw_cbore_diameter, m.set_screw_cbore_depth)
)

knurl = (
    cq.Workplane("YZ")
    .center(shaft_radius - m.knurl_depth/2.0, shaft_length/2.0)
    .rect(m.knurl_width, m.knurl_depth)
    .polarArray(radius=shaft_radius - m.knurl_depth/2.0, count=m.knurl_count, startAngle=0, angle=360)
    .extrude(m.knurl_depth)
)

pin = pin.cut(knurl)

result = pin