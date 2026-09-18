import cadquery as cq

# Parameters
max_dim = 100.0

total_length = 80.0
shoulder_length = 20.0
shaft_radius = 15.0
shoulder_radius = 30.0
channel_radius = 8.0
channel_length = total_length + 10.0
vent_slot_width = 12.0
vent_slot_height = 6.0
vent_slot_depth = 8.0
chamfer_size = 1.0

# 1. Base solid by revolving composite profile
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(shaft_radius, 0)
    .lineTo(shaft_radius, shoulder_length)
    .lineTo(shoulder_radius, shoulder_length)
    .lineTo(shoulder_radius, total_length)
    .lineTo(0, total_length)
    .close()
)
solid = profile.revolve(360)

# 2. Cut internal cylindrical channel
channel = (
    cq.Workplane("XY")
    .circle(channel_radius)
    .extrude(channel_length, both=True)
)
solid = solid.cut(channel)

# 3. Chamfer channel entry on top face edges
solid = solid.faces(">Z").edges().chamfer(chamfer_size)

# 4. Vent slot on shoulder surface
mid_z = shoulder_length + (total_length - shoulder_length) / 2
vent_slot = (
    cq.Workplane("XY")
    .center(shoulder_radius - vent_slot_depth/2, 0)
    .rect(vent_slot_width, vent_slot_height)
    .extrude(vent_slot_depth)
    .translate((0, 0, mid_z))
)
solid = solid.cut(vent_slot)

result = solid