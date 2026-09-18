import cadquery as cq

# Parameters
base_width = 80.0
base_depth = 30.0
base_thickness = 8.0
base_corner_radius = 3.0
clip_wall_thickness = 2.0
clip_height = 25.0
clip_radius = 12.0
clip_hole_diameter = 6.0
clip_hole_offset = 5.0
pocket_width = 20.0
pocket_depth = 10.0
pocket_height = 4.0
pocket_offset_x = 0.0
pocket_offset_y = -5.0
chamfer_distance = 1.0

# Base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# Clip profile (closed wire) on XZ plane
clip_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, clip_height)
    .threePointArc((clip_radius, clip_height/2), (0, 0))
    .close()
)

# Extrude clip profile to give wall thickness
clip_body = (
    clip_profile
    .extrude(clip_wall_thickness)
)

# Add a through hole in the clip body
clip_body = (
    clip_body
    .faces(">Z")
    .workplane()
    .center(clip_hole_offset, 0)
    .hole(clip_hole_diameter)
)

# Position clip on the side of the base plate
clip_positioned = (
    clip_body
    .translate((base_width/2 - clip_wall_thickness/2, 0, base_thickness/2))
)

# Combine base and clip
assembly = base.union(clip_positioned)

# Recessed pocket on top surface of base plate
assembly = (
    assembly
    .faces(">Z")
    .workplane()
    .center(pocket_offset_x, pocket_offset_y)
    .rect(pocket_width, pocket_depth)
    .cutBlind(pocket_height)
)

# Chamfer outer vertical edges of the clip for safety
assembly = (
    assembly
    .edges("|Z and >X")
    .chamfer(chamfer_distance)
)

result = assembly