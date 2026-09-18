import cadquery as cq
from types import SimpleNamespace as Measures

measures = Measures(
    pin_length=45.0,
    pin_diameter=6.0,
    flare_length=10.0,
    flare_diameter=12.0,
    screw_hole_diameter=2.5,
    screw_cbore_diameter=5.0,
    screw_cbore_depth=3.0,
    side_slot_width=2.0,
    side_slot_depth=1.5,
    hex_boss_size=4.0,
    hex_boss_height=1.0
)

m = measures

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(m.pin_diameter / 2, 0)
    .lineTo(m.pin_diameter / 2, m.pin_length)
    .lineTo(m.flare_diameter / 2, m.pin_length)
    .lineTo(m.flare_diameter / 2, m.pin_length + m.flare_length)
    .lineTo(0, m.pin_length + m.flare_length)
    .close()
)

pin_body = profile.revolve()

boss_offset = m.pin_diameter / 2 - m.hex_boss_size / 2
hex_boss = (
    cq.Workplane('YZ')
    .center(boss_offset, m.pin_length / 2)
    .polygon(6, m.hex_boss_size)
    .extrude(m.hex_boss_height)
)

hex_boss = (
    hex_boss.faces('>X').workplane()
    .rect(m.side_slot_width, m.side_slot_depth)
    .cutBlind(-m.side_slot_depth)
)

combined = pin_body.union(hex_boss)

result = (
    combined
    .faces('>Z').workplane()
    .cboreHole(m.screw_hole_diameter, m.screw_cbore_diameter, m.screw_cbore_depth)
)
