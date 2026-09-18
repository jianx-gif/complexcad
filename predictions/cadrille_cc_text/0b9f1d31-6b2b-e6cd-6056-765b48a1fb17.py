import cadquery as cq
pipe_inner_radius = 8.0
wall_thickness = 2.0
block_height = 6.0
block_width = 8.0
block_length = 12.0
chamfer_size = 1.0
hole_diameter = 3.0
hole_clearance = 2.0
mount_hole_diameter = 4.0
mount_hole_block_dia = 3.0
mount_hole_offset = block_height / 2.0
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(pipe_inner_radius, 0)
    .lineTo(pipe_inner_radius, block_height)
    .lineTo(block_width, block_height)
    .lineTo(block_width, block_height + block_height)
    .lineTo(0, block_height + block_height)
    .close()
    .extrude(block_length)
    .shell(-wall_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
block = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(hole_diameter / 2.0)
    .extrude(block_length)
    .translate((0, 0, block_height / 2.0))
)
block = block.cut(block)
block = (
    block.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter)
)
result = block
