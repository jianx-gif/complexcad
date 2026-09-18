import cadquery as cq
block_width = 60.0
block_depth = 20.0
block_height = 25.0
arc_diameter = 100.0
cutout_radius = 20.0
cutout_diameter = 4.0
cutout_radius = cutout_radius + cutout_radius
chamfer_dist = 1.0
hole_offset_x = 15.0
hole_offset_y = 10.0
hole_count = 6
hole_offset_y = block_depth / 2.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(block_width, 0)
    .lineTo(block_width, block_height)
    .lineTo(block_width - block_depth, block_height)
    .lineTo(block_width - block_depth, block_height + block_height)
    .lineTo(block_width - block_depth, block_height + block_height)
    .lineTo(block_width - block_depth, block_height + block_height)
    .lineTo(block_width - block_depth, block_height + block_height)
    .lineTo(block_width - block_depth, block_height + block_height)
    .lineTo(block_width - block_depth, block_height + block_height)
    .lineTo(block_width - block_depth, block_height + block_height)
    .lineTo(0, block_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_dist)
hole_positions = [(-hole_offset_x, hole_offset_y), (hole_offset_x, hole_offset_y)]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cboreHole(hole_diameter, cutout_radius, cutout_radius)
)
result = solid
