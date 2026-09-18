import cadquery as cq
import math

# Parameters
base_width = 80.0
base_depth = 40.0
base_thickness = 5.0
base_corner_radius = 3.0
clip_length = 60.0
clip_height = 30.0
clip_thickness = 5.0
clip_taper_angle = 15.0  # degrees
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 4
hole_offset_from_base = 10.0
chamfer_distance = 1.0
fillet_radius = 2.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# Clip profile (trapezoid) on XY plane
half_base = clip_height / 2.0
half_top = half_base - clip_length * math.tan(math.radians(clip_taper_angle))
clip_profile = (
    cq.Workplane("XY")
    .polyline([
        (-half_base, 0),
        (half_base, 0),
        (half_top, clip_length),
        (-half_top, clip_length),
    ])
    .close()
)

# Extrude clip and position it on top of base
clip = (
    clip_profile
    .extrude(clip_thickness)
    .translate((0, base_depth/2.0, base_thickness))
)

# Add patterned holes on the front face of the clip
clip_with_holes = (
    clip
    .faces(">Y")
    .workplane()
    .center(0, hole_offset_from_base)
    .rarray(0, hole_spacing, 1, hole_count)
    .circle(hole_diameter/2.0)
    .cutBlind(clip_thickness + 0.1)
)

# Chamfer the leading edge of the clip (front face edges)
clip_chamfered = (
    clip_with_holes
    .faces(">Y")
    .edges()
    .chamfer(chamfer_distance)
)

# Fillet the vertical edges of the clip for safety
clip_fillet = (
    clip_chamfered
    .edges("|Z")
    .fillet(fillet_radius)
)

# Combine base and clip
result = base.union(clip_fillet)
