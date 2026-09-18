import cadquery as cq
outer_size = 80.0
wall_thickness = 2.0
channel_length = 100.0
channel_width = wall_thickness
countersink_angle = 90.0
countersink_diameter = 5.5
hole_diameter = 3.2
hole_spacing = 25.0
hole_count = 6
chamfer_distance = 1.0
rib_width = 10.0
rib_height = 5.0
rib_length = outer_size - 2 * wall_thickness
base = (
    cq.Workplane("XY")
    .rect(outer_size, outer_size)
    .extrude(channel_width)
)
channel = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(channel_width, channel_length)
    .extrude(channel_width)
)
channel = (
    channel.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(channel_width, channel_length)
    .extrude(channel_width)
)
channel = channel.edges("|Z").chamfer(chamfer_distance)
channel = channel.faces(">Z").edges().chamfer(chamfer_distance)
channel = channel.faces(">Z").workplane()
channel = channel.edges("|Z").chamfer(chamfer_distance)
channel = channel.edges("|Z").chamfer(chamfer_distance)
channel = channel.faces(">Z").workplane()
result = channel
