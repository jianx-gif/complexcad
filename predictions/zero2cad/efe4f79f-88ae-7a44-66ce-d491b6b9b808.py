import cadquery as cq

# Parameters
channel_length = 100.0
channel_width = 30.0
channel_height = 20.0
wall_thickness = 1.0
tab_width = 5.0
tab_height = 8.0
pocket_width = 12.0
pocket_height = 10.0
pocket_depth = 4.0
hole_diameter = 3.2
hole_spacing_x = 15.0
hole_spacing_y = 12.0
hole_rows = 3
hole_cols = 4
chamfer_size = 0.5

# Base profile with side tab
profile = (
    cq.Workplane("XY")
    .moveTo(-channel_width/2, -channel_height/2)
    .lineTo(channel_width/2 - tab_width, -channel_height/2)
    .lineTo(channel_width/2 - tab_width, -channel_height/2 + (channel_height - tab_height)/2)
    .lineTo(channel_width/2, -channel_height/2 + (channel_height - tab_height)/2)
    .lineTo(channel_width/2, -channel_height/2 + (channel_height + tab_height)/2)
    .lineTo(channel_width/2 - tab_width, -channel_height/2 + (channel_height + tab_height)/2)
    .lineTo(channel_width/2 - tab_width, channel_height/2)
    .lineTo(-channel_width/2, channel_height/2)
    .close()
)

# Extrude and shell to create thin-walled channel
result = (
    profile
    .extrude(channel_length)
    .shell(-wall_thickness)
)

# Add side pocket on +X face
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)

# Drill grid of holes on +Y face
result = (
    result
    .faces(">Y")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter)
)

# Chamfer outer edges
result = (
    result
    .edges("|Z")
    .chamfer(chamfer_size)
)
