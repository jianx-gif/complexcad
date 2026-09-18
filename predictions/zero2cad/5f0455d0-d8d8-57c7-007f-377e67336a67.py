import cadquery as cq

# Parameters
block_length = 80.0
block_width = 40.0
block_height = 30.0
wall_thickness = 4.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_spacing = 25.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 10.0
rib_spacing = 12.0
rib_depth = 3.0
tab_length = 12.0
tab_width = 20.0
tab_height = 15.0

# Base block
result = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
)

# Chamfer front face edges
result = (
    result
    .faces(">X")
    .edges()
    .chamfer(chamfer_distance)
)

# Mounting holes on front face
hole_positions = [
    (-hole_spacing / 2, hole_offset),
    (hole_spacing / 2, hole_offset),
]
result = (
    result
    .faces(">X")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Internal ribs on top face (cut pockets)
rib_count = int((block_length - 2 * wall_thickness) // rib_spacing)
rib_start = -block_length / 2 + wall_thickness + rib_spacing / 2
rib_positions = [rib_start + i * rib_spacing for i in range(rib_count)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(x, 0) for x in rib_positions])
    .rect(rib_width, rib_height)
    .cutBlind(rib_depth)
)

# Side tab on front face
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(tab_width, tab_height)
    .extrude(tab_length)
)
