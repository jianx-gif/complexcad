import cadquery as cq

# Parameters
channel_length = 80.0
channel_height = 30.0
channel_top_width = 30.0
channel_bottom_width = 15.0
wall_thickness = 2.0
rib_thickness = 3.0
rib_height = 10.0
rib_offset_from_bottom = 5.0
chamfer_distance = 1.5

# Outer trapezoidal profile on YZ plane
outer_profile = (
    cq.Workplane("YZ")
    .polyline([
        (-channel_top_width/2, 0),
        (channel_top_width/2, 0),
        (channel_bottom_width/2, channel_height),
        (-channel_bottom_width/2, channel_height),
    ])
    .close()
)

# Extrude to create solid channel
solid_channel = outer_profile.extrude(channel_length)

# Shell to create thin-walled channel
hollow_channel = solid_channel.shell(-wall_thickness)

# Internal rib positioned against inner left wall
rib = (
    cq.Workplane("YZ")
    .rect(rib_thickness, rib_height)
    .extrude(channel_length)
    .translate((0, -channel_top_width/2 + wall_thickness + rib_thickness/2, rib_offset_from_bottom + rib_height/2))
)

# Combine rib with hollow channel
combined = hollow_channel.union(rib)

# Chamfer entry face (front face at X=0)
result = (
    combined
    .faces("<X")
    .edges()
    .chamfer(chamfer_distance)
)
