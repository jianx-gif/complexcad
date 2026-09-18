import cadquery as cq

# Parameters
channel_length = 80.0
outer_width = 40.0
outer_height = 30.0
wall_thickness = 1.5
notch_width = 10.0
notch_depth = 5.0
notch_start = (outer_width - notch_width) / 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 3
rib_width = 6.0
rib_thickness = 2.0
rib_depth = 4.0

# Build outer profile with notch
profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(outer_width, 0)
    .lineTo(outer_width, outer_height)
    .lineTo(notch_start + notch_width, outer_height)
    .lineTo(notch_start + notch_width, outer_height - notch_depth)
    .lineTo(notch_start, outer_height - notch_depth)
    .lineTo(notch_start, outer_height)
    .lineTo(0, outer_height)
    .close()
)

# Extrude to create channel
result = (
    profile
    .extrude(channel_length)
    # Thin-walled shell
    .shell(-wall_thickness, kind="intersection")
    # Chamfer outer longitudinal edges (parallel to X)
    .edges("|X")
    .chamfer(chamfer_distance)
    # Add mounting holes on inner side wall (facing -Y direction)
    .faces("<Y")
    .workplane()
    .center(0, -((hole_count - 1) * hole_spacing) / 2.0)
    .rarray(0, hole_spacing, 1, hole_count)
    .hole(hole_diameter)
    # Add internal rib on inner bottom face for stiffness
    .faces("<Z")
    .workplane()
    .center(0, -outer_height/2 + wall_thickness + rib_depth/2)
    .rect(rib_width, rib_thickness)
    .cutBlind(-rib_depth)
)
