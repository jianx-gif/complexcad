import cadquery as cq

# Parameters
block_length = 80.0
block_width = 40.0
block_height = 15.0
corner_radius = 5.0
chamfer_distance = 1.0
hole_diameter = 8.0
hole_depth = 10.0
hole_offset_x = 0.0
hole_offset_y = -10.0
slot_width = 5.0
slot_length = 30.0
slot_depth = 12.0
slot_offset_x = -20.0
slot_offset_y = 0.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 3

# Base block with rounded corners and chamfered edges
base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .edges("|Z")
    .fillet(corner_radius)
    .edges()
    .chamfer(chamfer_distance)
)

# Blind hole on top face
with_hole = (
    base
    .faces(">Z")
    .workplane()
    .center(hole_offset_x, hole_offset_y)
    .hole(hole_diameter, depth=hole_depth)
)

# Side slot on top face
with_slot = (
    with_hole
    .faces(">Z")
    .workplane()
    .center(slot_offset_x, slot_offset_y)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)

# Rib profile (to be cut into the block)
rib_profile = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(block_height)
)

# Create rib array and cut from the part
rib_array = (
    rib_profile
    .rarray(rib_spacing, 0, rib_count, 1)
    .translate((-(block_length/2) + rib_spacing/2, 0, 0))
)

result = with_slot.cut(rib_array)
