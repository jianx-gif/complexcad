import cadquery as cq

# Parameters
channel_length = 80.0
channel_height = 40.0
channel_width = 20.0
wall_thickness = 1.0
notch_width = 10.0
notch_depth = 5.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 5
chamfer_size = 0.5

# Build outer profile with a top notch
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(channel_length, 0)
    .lineTo(channel_length, channel_height)
    .lineTo(channel_length - notch_width, channel_height)
    .lineTo(channel_length - notch_width, channel_height - notch_depth)
    .lineTo(notch_width, channel_height - notch_depth)
    .lineTo(notch_width, channel_height)
    .lineTo(0, channel_height)
    .close()
)

# Extrude to create solid channel
solid = profile.extrude(channel_width)

# Shell to make thin-walled channel
hollow = solid.shell(-wall_thickness)

# Add linear array of screw holes on the +Y side wall
holes = (
    hollow.faces(">Y")
    .workplane()
    .rarray(hole_spacing, 0, hole_count, 1, center=True)
    .hole(hole_diameter)
)

# Apply chamfer to outer edges for safety
result = (
    holes.edges("|Z")
    .chamfer(chamfer_size)
)
