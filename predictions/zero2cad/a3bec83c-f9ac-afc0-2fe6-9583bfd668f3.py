import cadquery as cq

# Parameters
base_width = 80.0
base_depth = 40.0
base_thickness = 4.0
base_corner_radius = 5.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_offset_y = 10.0
clip_wall_thickness = 2.0
clip_height = 12.0
clip_length = 30.0
clip_arc_radius = 15.0
clip_chamfer = 1.0

# Base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# Mounting holes (four holes in a rectangular pattern)
mount_holes = (
    cq.Workplane("XY")
    .pushPoints([
        (-mount_hole_spacing/2, mount_hole_offset_y),
        (mount_hole_spacing/2, mount_hole_offset_y),
        (-mount_hole_spacing/2, -mount_hole_offset_y),
        (mount_hole_spacing/2, -mount_hole_offset_y),
    ])
    .circle(mount_hole_diameter/2)
    .extrude(base_thickness + 1)
)

# Clip profile (closed wire) on XY plane
clip_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, clip_height)
    .threePointArc((clip_arc_radius, clip_height + clip_arc_radius), (clip_length, clip_height))
    .lineTo(clip_length, 0)
    .close()
)

# Extrude clip and position it on the front edge of the base
clip = (
    clip_profile
    .extrude(clip_wall_thickness)
    .translate((0, -base_depth/2, base_thickness))
)

# Chamfer the leading edge of the clip (edges parallel to Y)
clip = (
    clip
    .edges("|Y")
    .chamfer(clip_chamfer)
)

# Assemble final part
result = (
    base
    .cut(mount_holes)
    .union(clip)
)
