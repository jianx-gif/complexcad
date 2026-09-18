import cadquery as cq
bracket_length = 80.0
bracket_height = 20.0
channel_width = 30.0
channel_height = 20.0
wall_thickness = 5.0
fillet_radius = 2.0
countersink_angle = 82.0
hole_diameter = 5.0
countersink_diameter = 9.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 1.0
rib_height = 6.0
rib_thickness = 4.0
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_height)
    .extrude(bracket_width)
)
channel = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(channel_width, channel_height)
    .extrude(bracket_width)
)
channel = base.cut(channel)
channel = channel.edges("|Z").fillet(fillet_radius)
channel = channel.edges("|Z").chamfer(chamfer_size)
channel = channel.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (channel_length/2 - hole_offset,  channel_height/2 - hole_offset),
    (-channel_length/2 + hole_offset,  channel_height/2 - hole_offset),
    (channel_length/2 - hole_offset,  channel_height/2 - hole_offset),
]
channel = (
    channel.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, depth=channel_height)
)
channel = channel.edges("|Z").chamfer(chamfer_size)
channel = channel.edges("|Z").chamfer(chamfer_size)
channel = channel.edges("|Z").fillet(fillet_radius)
result = channel
