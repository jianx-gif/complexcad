import cadquery as cq

outer_radius = 40.0
inner_radius = 25.0
block_height = 50.0
boss_radius = 15.0
boss_height = 15.0
counterbore_diameter = 20.0
counterbore_depth = 10.0
through_hole_diameter = 8.0
chamfer_size = 1.0
slot_width = 5.0
slot_length = 30.0
slot_depth = 5.0

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, block_height)
    .lineTo(boss_radius, block_height)
    .lineTo(boss_radius, block_height + boss_height)
    .lineTo(inner_radius, block_height + boss_height)
    .close()
)

solid = profile.revolve()

solid = (
    solid
    .faces(">Z")
    .workplane()
    .hole(counterbore_diameter, depth=counterbore_depth)
    .hole(through_hole_diameter)
)

solid = (
    solid
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(slot_depth)
)

solid = solid.edges().chamfer(chamfer_size)

result = solid