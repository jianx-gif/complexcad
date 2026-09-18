import cadquery as cq

# Parameters
block_length = 80.0
block_width = 50.0
block_height = 12.0
wall_thickness = 4.0
rib_height = 6.0
rib_width = 30.0
rib_thickness = 4.0
rib_offset = 2.0
slot_width = 2.0
slot_length = 10.0
slot_spacing = 15.0
slot_count = 3
chamfer_size = 0.8

# Base block with chamfered vertical edges
base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Internal cavity (subtract to create walls)
inner_cavity = (
    cq.Workplane("XY")
    .rect(block_length - 2 * wall_thickness, block_width - 2 * wall_thickness)
    .extrude(block_height - wall_thickness)
    .translate((0, 0, wall_thickness))
)

# Side rib on +X face
rib = (
    base.faces(">X")
    .workplane()
    .center(0, rib_offset + rib_thickness / 2)
    .rect(rib_width, block_height - 2 * rib_offset)
    .extrude(rib_height)
)

# Combine base, rib, and cut cavity
combined = base.union(rib).cut(inner_cavity)

# Vent slots on top face
result = (
    combined.faces(">Z")
    .workplane()
    .rarray(slot_spacing, 0, slot_count, 1)
    .rect(slot_width, slot_length)
    .cutBlind(-wall_thickness)
)
