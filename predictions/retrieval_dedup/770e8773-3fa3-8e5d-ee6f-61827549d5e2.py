import cadquery as cq
from types import SimpleNamespace as Measures

measures = Measures(
    shank_length=30.0,
    shank_radius=5.0,
    head_radius=10.0,
    head_height=6.0,
    fillet_radius=2.0,
    pilot_diameter=2.0,
    knurl_depth=1.0,
    knurl_width=2.0,
    knurl_length=3.0,
    knurl_pitch=2.0,
    knurl_rows=5,
    knurl_per_row=12
)
m = measures

base_wp = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(m.shank_radius, 0)
    .lineTo(m.shank_radius, m.shank_length)
    .lineTo(m.head_radius, m.shank_length)
    .lineTo(m.head_radius, m.shank_length + m.head_height)
    .lineTo(0, m.shank_length + m.head_height)
    .close()
    .revolve()
)

base_wp = base_wp.faces(">Z").edges().fillet(m.fillet_radius)

base_wp = (
    base_wp.faces(">Z").workplane()
    .hole(m.pilot_diameter)
)

base = base_wp.val()

result_wp = cq.Workplane().add(base)
angle_step = 360.0 / m.knurl_per_row
for row in range(m.knurl_rows):
    z_offset = row * m.knurl_pitch
    for n in range(m.knurl_per_row):
        angle = n * angle_step
        tooth = (
            cq.Workplane('XY')
            .rect(m.knurl_depth, m.knurl_width)
            .extrude(m.knurl_length)
            .transformed(
                rotate=(0, 0, angle),
                offset=(m.shank_radius + m.knurl_depth/2.0, 0, z_offset)
            )
        ).val()
        result_wp = result_wp.add(tooth)

result = result_wp.combine()
