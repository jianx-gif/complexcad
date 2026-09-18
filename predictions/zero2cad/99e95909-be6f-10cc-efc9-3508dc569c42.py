import cadquery as cq

# Parameters
base_width = 80.0
base_depth = 40.0
base_thickness = 5.0
base_corner_radius = 3.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 6.0
rib_count = int((base_width - 2 * rib_spacing) // (rib_width + rib_spacing))
clip_wall_thickness = 2.0
clip_height = 12.0
clip_length = 30.0
clip_arc_radius = 10.0
clip_chamfer = 1.0
edge_fillet = 0.8

# Base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# Ribbed extrusion on top surface
rib_pattern = (
    base.faces(">Z")
    .workplane()
    .rarray(rib_width + rib_spacing, 0, rib_count, 1, center=True)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)

# Clip profile (closed wire) on XZ plane
clip_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, clip_height)
    .threePointArc((clip_arc_radius, clip_height + clip_arc_radius), (clip_length, clip_height))
    .lineTo(clip_length, 0)
    .close()
)

# Sweep path along Y direction
clip_path = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, clip_length)
    .wire()
)

# Sweep the profile along the path
clip = (
    clip_profile
    .sweep(clip_path, transition="round")
    .translate((0, -base_depth/2, base_thickness))
)

# Assemble all components
result = (
    base
    .union(rib_pattern)
    .union(clip)
    .edges("|Y")
    .chamfer(clip_chamfer)
    .edges(">Z")
    .fillet(edge_fillet)
)
