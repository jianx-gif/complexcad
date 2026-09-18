import cadquery as cq
channel_length = 80.0
channel_width = 20.0
channel_height = 40.0
wall_thickness = 1.0
notch_width = 10.0
notch_depth = 5.0
edge_chamfer = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(channel_length, 0)
    .lineTo(channel_length, channel_height)
    .lineTo(channel_length - notch_width, channel_height)
    .lineTo(channel_length - notch_width, channel_height - notch_depth)
    .lineTo(channel_length - notch_width, channel_height)
    .lineTo(channel_length - notch_width, channel_height)
    .lineTo(channel_length, 0)
    .lineTo(channel_length, 0)
    .close()
    .extrude(channel_depth)
)
notch = (
    base.faces(">X").workplane()
    .center(0, 0)
    .rarray(hole_spacing, 0, 2, 1)
    .hole(hole_diameter)
)
result = (
    not_face
    .edges("|Z")
    .chamfer(edge_chamfer)
)
