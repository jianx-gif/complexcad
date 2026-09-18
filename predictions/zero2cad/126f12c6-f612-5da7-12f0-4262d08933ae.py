import cadquery as cq

# Parameters
block_length = 80.0
block_width = 50.0
block_height = 25.0
wall_thickness = 3.0
rib_thickness = 2.0
rib_spacing = 10.0
rib_height = block_height - 2 * wall_thickness
rib_length = block_width - 2 * wall_thickness
rib_count = int((block_length - 2 * wall_thickness) // rib_spacing)
chamfer_size = 0.8
hole_diameter = 12.0

# Base block with central through hole
base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Shell to create thin walls
shelled = base.shell(-wall_thickness)

# Internal ribs on the bottom interior face
ribs = (
    shelled.faces("<Z")
    .workplane()
    .center(wall_thickness + rib_spacing / 2, 0)
    .rect(rib_length, rib_thickness)
    .rarray(rib_spacing, 0, rib_count, 1)
    .extrude(rib_height)
)

# Combine ribs with shelled block
combined = shelled.union(ribs)

# Chamfer top outer edges for safety
result = combined.faces(">Z").edges().chamfer(chamfer_size)
