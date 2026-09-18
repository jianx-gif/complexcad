import cadquery as cq
block_width = 40.0
block_height = 20.0
block_thickness = 5.0
sweep_angle = 120.0
sweep_angle = 360.0
sweep_angle = 360.0
chamfer_distance = 1.0
pocket_width = 15.0
pocket_depth = 8.0
pocket_thickness = 5.0
clearance_dia = 4.5
hole_offset_x = 12.0
hole_offset_y = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(block_width, 0)
    .lineTo(block_width, block_height - arc_height)
    .lineTo(block_width - arc_height, block_height - arc_height)
    .lineTo(block_width - arc_height, block_height)
    .lineTo(block_width - arc_height, block_height - arc_height)
    .lineTo(block_width, block_height)
    .lineTo(0, block_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
hole_positions = [
    (hole_offset_x, hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, -hole_offset_y),
    (hole_offset_x, -hole_offset_y),
]
solid = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(clearance_dia)
)
result = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(clearance_dia)
)
