import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 12.0
height = 50.0
tip_height = 8.0
tip_radius = 8.0
chamfer_dist = 1.2
slot_width = 4.0
slot_depth = 6.0
slot_height = 20.0
slot_count = 6

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height - tip_height)
    .lineTo(tip_radius, height)
    .lineTo(0, height)
    .close()
)

# Revolve to create axisymmetric body
body = profile.revolve()

# Central bore through entire part
body = body.faces("<Z").workplane().hole(inner_radius * 2)

# Create a single slot solid positioned at mid-height
slot = (
    cq.Workplane("XY")
    .center(outer_radius - slot_depth / 2, 0)
    .rect(slot_width, slot_depth)
    .extrude(slot_height)
    .translate((0, 0, (height - slot_height) / 2))
)

# Cut slots around the circumference
for i in range(slot_count):
    angle = i * 360.0 / slot_count
    body = body.cut(slot.rotate((0, 0, 0), (0, 0, 1), angle))

# Apply chamfer to all edges for safety
body = body.edges().chamfer(chamfer_dist)

result = body