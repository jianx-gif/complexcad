import cadquery as cq
pin_length = 45.0
pin_diameter = 6.0
corner_length = 10.0
corner_diameter = 12.0
screw_hole_diameter = 2.5
screw_cbore_diameter = 5.0
screw_cbore_depth = 3.0
hex_boss_height = 1.0
hex_boss_width = hex_boss_width * 0.6
hex_boss_depth = hex_boss_height * 0.6
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(pin_length, 0)
    .lineTo(pin_length, pin_diameter)
    .lineTo(pin_length - corner_length, pin_diameter)
    .lineTo(pin_length - corner_length, pin_diameter - corner_length)
    .lineTo(pin_length, pin_diameter - corner_length)
    .lineTo(pin_length, pin_diameter)
    .lineTo(0, pin_diameter)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(corner_length)
solid = (
    solid.faces(">Z")
    .workplane()
    .center(0, 0)
    .polygon(6, hex_boss_width)
    .cutBlind(-hex_boss_depth)
)
solid = (
    solid.faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(screw_hole_diameter, screw_cbore_diameter, screw_cbore_depth)
)
result = solid
