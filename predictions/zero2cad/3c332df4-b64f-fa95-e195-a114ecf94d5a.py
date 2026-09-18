import cadquery as cq

# Parameters
channel_length = 80.0
channel_height = 40.0
channel_width = 30.0
wall_thickness = 1.5
rib_thickness = 1.2
rib_height = channel_height - 2 * wall_thickness
rib_length = channel_length - 2 * wall_thickness
hole_diameter = 3.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 0.6

# Base solid: rectangular block
base = (
    cq.Workplane("XZ")
    .lineTo(0, channel_height)
    .lineTo(channel_length, channel_height)
    .lineTo(channel_length, 0)
    .close()
    .extrude(channel_width)
)

# Thin-walled channel via shell
channel = base.shell(-wall_thickness)

# Chamfer outer edges for safety
channel = channel.edges().chamfer(chamfer_size)

# Add internal rib on the +Y inner wall
rib = (
    channel.faces(">Y")
    .workplane()
    .rect(rib_length, rib_height)
    .extrude(rib_thickness, combine=True)
)

# Drill four M3 holes on the +Y inner wall
hole_positions = [
    (hole_offset, hole_offset),
    (hole_offset + hole_spacing, hole_offset),
    (hole_offset, hole_offset + hole_spacing),
    (hole_offset + hole_spacing, hole_offset + hole_spacing),
]
result = (
    rib.faces(">Y")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
