import cadquery as cq

# Parameters
channel_length = 80.0  # length of channel
channel_width = 30.0   # overall width (flange span)
channel_height = 20.0  # overall height of channel cross-section
wall_thickness = 3.0   # shell wall thickness
web_thickness = 6.0    # thickness of internal stiffening web
rim_chamfer = 2.0      # chamfer size for rim edges

# Base solid: rectangular prism to be turned into a hollow channel
base_box = (
    cq.Workplane("XY")
    .box(channel_length, channel_width, channel_height, centered=(True, True, False))
)

# Create hollow by shelling inward
hollow_shell = base_box.shell(-wall_thickness)

# Internal stiffening web: runs the length of the channel, centered in Y, filling interior height
stiffening_web = (
    cq.Workplane("XY")
    .box(channel_length, web_thickness, channel_height - 2 * wall_thickness, centered=(True, True, False))
    .translate((0, 0, wall_thickness))
)

# Combine shell and web
combined = hollow_shell.union(stiffening_web)

# Apply chamfer to the outer rim edges (top and bottom edges along X direction)
result = (
    combined
    .edges("(>Z or <Z) and |X")
    .chamfer(rim_chamfer)
)
