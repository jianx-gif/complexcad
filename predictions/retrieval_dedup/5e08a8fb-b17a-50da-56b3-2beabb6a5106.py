import cadquery as cq

# Parameters
block_length = 80.0
block_width = 40.0
block_height = 20.0
slot_width = 12.0
slot_length = 60.0
slot_depth = 12.0
slot_chamfer = 2.0
hole_diameter = 8.0
hole_offset_x = 0.0
hole_offset_y = 0.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 20.0
outer_chamfer = 1.0

# Base block
result = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
)

# Milled slot cut into the top face
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)

# Chamfer the slot entrance edges on the top face
result = (
    result
    .faces(">Z")
    .edges()
    .chamfer(slot_chamfer)
)

# Through hole through the entire block, centered
result = (
    result
    .faces("<Z")
    .workplane()
    .center(hole_offset_x, hole_offset_y)
    .hole(hole_diameter)
)

# Reinforcing ribs on the bottom face, spaced along length
rib_count = int((block_length - rib_spacing) // rib_spacing) + 1
for i in range(rib_count):
    x_pos = -block_length / 2 + rib_spacing / 2 + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .rect(rib_width, block_width)
        .extrude(rib_height)
        .translate((x_pos, 0, 0))
    )
    result = result.union(rib)

# Chamfer outer edges of the block for safety
result = result.edges(">Z").chamfer(outer_chamfer)
