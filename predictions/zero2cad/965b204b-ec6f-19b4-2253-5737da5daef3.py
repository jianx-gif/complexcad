import cadquery as cq

# Parameters
base_width = 70.0
base_depth = 30.0
base_thickness = 3.0
base_corner_radius = 2.0
clip_arm_length = 20.0
clip_arm_width = 10.0
clip_arm_thickness = 2.5
clip_arm_offset = 5.0
pocket_width = 20.0
pocket_depth = 12.0
pocket_height = 1.5
pocket_fillet_radius = 0.8
chamfer_distance = 2.0

# Base plate with chamfer on front edge
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|X and >Z")
    .chamfer(chamfer_distance)
)

# Clip arm attached to front edge
clip_arm = (
    cq.Workplane("XY")
    .center(base_width/2 - clip_arm_offset - clip_arm_width/2, base_depth/2)
    .rect(clip_arm_width, clip_arm_length)
    .extrude(clip_arm_thickness)
    .translate((0, 0, base_thickness))
)

# Combine base and clip arm
combined = base.union(clip_arm)

# Recessed pocket on top surface
pocket = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_depth)
    .cutBlind(pocket_height)
)

# Fillet pocket interior vertical edges
result = (
    pocket
    .edges("|Z")
    .fillet(pocket_fillet_radius)
)
