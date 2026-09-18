import cadquery as cq
outer_diameter = 80.0
inner_diameter_step1 = 30.0
inner_diameter_step2 = 40.0
block_height = 60.0
block_width = 15.0
mount_hole_diameter = 8.0
mount_hole_offset = 20.0
chamfer_size = 2.0
relief_width = 15.0
relief_depth = 8.0
relief_height = block_height - 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter_step1, 0)
    .lineTo(inner_diameter_step2, 0)
    .lineTo(inner_diameter_step2, block_height)
    .lineTo(inner_diameter_step3, block_height)
    .lineTo(inner_diameter_step3, 0)
    .close()
)
block = profile.revolve()
block = (
    cq.Workplane("XY")
    .center(inner_diameter_step1, 0)
    .rect(block_width, block_height)
    .revolve()
    .edges()
    .chamfer(chamfer_size)
)
block = block.faces(">Z").workplane().hole(inner_diameter_step2)
block = (
    block.faces(">Z")
    .workplane()
    .center(mount_hole_offset, 0)
    .hole(mount_hole_diameter)
)
block = (
    block.faces(">Z")
    .workplane()
    .center(mount_hole_offset, 0)
    .hole(mount_hole_diameter)
)
result = block
