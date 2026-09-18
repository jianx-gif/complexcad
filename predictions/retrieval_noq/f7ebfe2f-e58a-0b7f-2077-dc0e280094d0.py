import cadquery as cq
from math import radians, cos, sin

# Base dimensions
base_width = 60.0
base_length = 40.0
base_thickness = 5.0
base_corner_radius = 3.0

# Clip dimensions (side view)
clip_width = 10.0          # height of cantilever (Y direction)
clip_length = 30.0         # length from base to tip (X direction)
snap_radius = 5.0          # visual reference
clip_depth = 3.0           # extrusion depth (Z direction)

# Pilot hole
pilot_hole_diameter = 3.0
pilot_hole_offset_y = -10.0

# Chamfer size
edge_chamfer = 0.5

# Overlap between clip root and base for fusion
clip_overlap = 0.5

# Base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_width, base_length)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# Clip side‑view profile and extrusion
clip_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, clip_width)
    .lineTo(clip_length - snap_radius, clip_width)
    .threePointArc((clip_length - snap_radius/2, clip_width*0.8), (clip_length, 0))
    .lineTo(0, 0)
    .close()
    .extrude(clip_depth)
    .edges()
    .chamfer(edge_chamfer)
)

# Position clip so it intersects the front edge of the base plate
clip_positioned = clip_profile.translate((0, base_length/2 - clip_overlap, base_thickness/2))

# Fuse base and clip
result = base.union(clip_positioned)

# Add pilot hole through the base plate
result = (
    result
    .faces("<Z")
    .workplane()
    .center(0, pilot_hole_offset_y)
    .circle(pilot_hole_diameter/2)
    .cutThruAll()
)
