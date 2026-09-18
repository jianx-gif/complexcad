import cadquery as cq
outer_radius = 45.0
block_height = 30.0
step_height = 5.0
step_thickness = 5.0
mount_hole_diameter = 6.0
mount_hole_count = 12
mount_hole_radius = outer_radius - 5.0
slot_width = 8.0
slot_length = 20.0
slot_depth = 5.0
slot_count = 4
slot_count = 3
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, block_height - step_height)
    .lineTo(outer_radius - step_height, block_height - step_height)
    .lineTo(outer_radius - step_height, block_height - step_height)
    .lineTo(0, block_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(2)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, count=slot_count, startAngle=0, angle=360)
    .hole(mount_hole_diameter)
)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, count=slot_count, startAngle=0, angle=360)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)
solid = solid.edges().fillet(2)
result = solid
