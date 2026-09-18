import cadquery as cq

# Parameters
block_length = 80.0
block_width = 60.0
block_thickness = 12.0
corner_fillet_radius = 5.0
boss_diameter = 30.0
boss_height = 20.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_thickness = 4.0
rib_height = 6.0
rib_spacing = 20.0
pocket_depth = 4.0
pocket_margin = 10.0

# Base block with filleted corners
base = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_thickness)
    .edges("|Z")
    .fillet(corner_fillet_radius)
)

# Central boss on top face
boss = (
    base.faces(">Z").workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Mounting holes at four corners (through entire part)
hole_positions = [
    (-block_length/2 + mount_hole_offset, -block_width/2 + mount_hole_offset),
    ( block_length/2 - mount_hole_offset, -block_width/2 + mount_hole_offset),
    ( block_length/2 - mount_hole_offset,  block_width/2 - mount_hole_offset),
    (-block_length/2 + mount_hole_offset,  block_width/2 - mount_hole_offset),
]
holes = (
    cq.Workplane("XY")
    .pushPoints(hole_positions)
    .circle(mount_hole_diameter / 2)
    .extrude(block_thickness + boss_height)
)

# Underside ribs for stiffness (grid pattern)
rib_grid = (
    cq.Workplane("XY")
    .rect(block_length - 2 * rib_spacing, block_width - 2 * rib_spacing)
    .vertices()
    .rect(rib_thickness, rib_thickness)
    .extrude(rib_height)
)

# Pocket on bottom face for weight reduction
pocket = (
    base.faces("<Z").workplane()
    .rect(block_length - 2 * pocket_margin, block_width - 2 * pocket_margin)
    .cutBlind(pocket_depth)
)

# Combine features
result = (
    base
    .union(boss)
    .cut(holes)
    .union(rib_grid)
    .cut(pocket)
)
