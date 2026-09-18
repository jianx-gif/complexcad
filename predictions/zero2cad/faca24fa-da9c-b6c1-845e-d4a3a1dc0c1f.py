import cadquery as cq

# Parameters
base_width = 80.0
base_depth = 30.0
base_thickness = 5.0
base_corner_radius = 0.8
mount_hole_diameter = 4.0
mount_hole_spacing = 20.0
clip_length = 40.0
clip_thickness = 3.0
clip_height = 12.0
rib_width = 2.0
rib_height = 4.0
rib_spacing = 6.0
rib_count = 6
rib_fillet_radius = 0.5
clearance_hole_diameter = 8.0
clearance_hole_offset_y = -10.0

# Base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# Mounting holes on top face
base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .circle(mount_hole_diameter/2)
    .cutThruAll()
)

# Clip body attached to back edge of base
clip_body = (
    cq.Workplane("XY")
    .center(0, -base_depth/2 - clip_height/2)
    .rect(clip_length, clip_height)
    .extrude(clip_thickness)
)

# Rib pattern on the front face of the clip
rib_pattern = (
    clip_body
    .faces(">Y")
    .workplane()
    .rarray(rib_spacing, 0, rib_count, 1)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
    .edges("|Y")
    .fillet(rib_fillet_radius)
)

# Clearance hole through the clip (through all thickness)
clip_with_hole = (
    rib_pattern
    .faces(">Z")
    .workplane()
    .center(0, clearance_hole_offset_y)
    .circle(clearance_hole_diameter/2)
    .cutThruAll()
)

# Assemble final part
result = base.union(clip_with_hole)
