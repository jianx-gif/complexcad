import cadquery as cq
import math

# Parameters
gear_length = 60.0
gear_diameter = 40.0
thread_pitch = 5.0
thread_depth = 4.0
thread_width = 3.0
flange_diameter = 60.0
flange_thickness = 10.0
flange_chamfer = 0.8
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = 20.0

# Derived values
gear_radius = gear_diameter / 2.0
flange_radius = flange_diameter / 2.0
thread_turns = gear_length / thread_pitch
thread_angle = 360.0 * thread_turns

# Base gear cylinder
gear_body = (
    cq.Workplane("XY")
    .circle(gear_radius)
    .extrude(gear_length)
)

# Flange with chamfer on outer edge
flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
    .edges()
    .chamfer(flange_chamfer)
)

# Combine gear and flange
combined = gear_body.union(flange)

# Thread profile (triangular) in XZ plane
thread_profile = (
    cq.Workplane("XZ")
    .moveTo(gear_radius - thread_depth, 0)
    .lineTo(gear_radius, thread_width / 2.0)
    .lineTo(gear_radius, -thread_width / 2.0)
    .close()
)

# Helical thread via twistExtrude
thread = (
    thread_profile
    .twistExtrude(gear_length, thread_angle)
)

# Add thread to combined part
combined = combined.union(thread)

# Mounting holes on flange (circular pattern)
hole_positions = []
for i in range(mount_hole_count):
    angle = i * 360.0 / mount_hole_count
    x = mount_hole_radius * math.cos(math.radians(angle))
    y = mount_hole_radius * math.sin(math.radians(angle))
    hole_positions.append((x, y))

combined = (
    combined
    .faces("<Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

result = combined