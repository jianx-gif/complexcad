import cadquery as cq

# Parameters
gear_diameter = 80.0
gear_width = 20.0
thread_pitch = 10.0
thread_depth = 5.0
num_starts = 2
chamfer_size = 1.0
slot_width = 4.0
slot_height = 6.0
slot_depth = 3.0
slot_count = 12

# Derived dimensions
gear_radius = gear_diameter / 2.0
thread_radius = gear_radius - thread_depth
twist_angle = 360.0 * gear_width / thread_pitch

# Base cylinder (gear body)
base = (
    cq.Workplane("XY")
    .circle(gear_radius)
    .extrude(gear_width)
)

# Thread profile (triangular) positioned at thread radius
thread_profile = (
    cq.Workplane("XY")
    .center(thread_radius, 0)
    .polyline([
        (0, 0),
        (thread_pitch / 2.0, thread_depth),
        (thread_pitch, 0),
    ])
    .close()
)

# Helical thread solid (single start)
thread_solid = thread_profile.twistExtrude(gear_width, twist_angle)

# Replicate thread for multiple starts
thread_union = thread_solid
for i in range(1, num_starts):
    angle = i * 360.0 / num_starts
    rotated = thread_solid.rotate((0, 0, 0), (0, 0, 1), angle)
    thread_union = thread_union.union(rotated)

# Combine base and threads
gear_body = base.union(thread_union)

# Chamfer outer edges on top and bottom faces
gear_body = gear_body.faces(">Z").edges().chamfer(chamfer_size)
gear_body = gear_body.faces("<Z").edges().chamfer(chamfer_size)

# Add patterned slots on the top face
result = (
    gear_body
    .faces(">Z")
    .workplane()
    .polarArray(radius=gear_radius - slot_depth / 2.0, startAngle=0, angle=360, count=slot_count)
    .rect(slot_width, slot_height)
    .cutBlind(-slot_depth)
)
