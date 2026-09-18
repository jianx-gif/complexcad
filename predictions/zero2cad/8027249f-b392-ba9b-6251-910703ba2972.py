import cadquery as cq

# Parameters
base_length = 80.0
base_width = 30.0
base_thickness = 5.0
base_corner_radius = 2.0
rib_width = 6.0
rib_height = 3.0
rib_spacing = 12.0
rib_count = 3
clip_thickness = 2.0
clip_height = 12.0
clip_length = 20.0
clip_fillet_radius = 0.8
clip_chamfer = 0.5

# Base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# Add ribs on top surface
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_length)
    .extrude(rib_height)
)

rib_pattern = (
    base
    .faces(">Z")
    .workplane()
    .rarray(0, rib_spacing, 1, rib_count)
    .add(rib)
)

# Create clip profile (non‑trivial closed shape)
clip_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(clip_thickness, 0)
    .lineTo(clip_thickness, clip_height - clip_thickness)
    .threePointArc((clip_thickness/2, clip_height), (0, clip_height - clip_thickness))
    .close()
)

# Extrude clip and position it on the side of the base
clip = (
    clip_profile
    .extrude(clip_length)
    .translate((0, base_width/2 + clip_thickness/2, base_thickness/2))
)

# Combine all features
result = (
    rib_pattern
    .union(clip)
    .edges("|Z")
    .fillet(clip_fillet_radius)
    .edges("<<Z and >Y")
    .chamfer(clip_chamfer)
)
