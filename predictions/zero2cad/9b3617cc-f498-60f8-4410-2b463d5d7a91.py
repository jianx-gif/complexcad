import cadquery as cq
import math

# Parameters
base_diameter = 60.0
base_thickness = 10.0
shoulder_diameter = 40.0
shoulder_height = 5.0
taper_length = 40.0
taper_end_diameter = 25.0
blind_hole_diameter = 6.0
blind_hole_depth = 30.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = 22.0
slot_width = 8.0
slot_length = 30.0
slot_depth = 5.0

# Derived dimensions
base_radius = base_diameter / 2.0
shoulder_radius = shoulder_diameter / 2.0
taper_end_radius = taper_end_diameter / 2.0

# Create revolved joint block profile
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_thickness)
    .lineTo(shoulder_radius, base_thickness + shoulder_height)
    .lineTo(taper_end_radius, base_thickness + shoulder_height + taper_length)
    .lineTo(0, base_thickness + shoulder_height + taper_length)
    .close()
)

# Revolve profile around Z axis
result = profile.revolve()

# Apply chamfer to all edges for safety
result = result.edges().chamfer(chamfer_size)

# Blind hole on top face (centered)
result = (
    result.faces(">Z")
    .workplane()
    .hole(blind_hole_diameter, blind_hole_depth)
)

# Mounting holes on bottom face arranged in a circle
mount_points = [
    (
        mount_hole_radius * math.cos(2 * math.pi * i / mount_hole_count),
        mount_hole_radius * math.sin(2 * math.pi * i / mount_hole_count),
    )
    for i in range(mount_hole_count)
]
result = (
    result.faces("<Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

# Rectangular slot on top face for cable routing
result = (
    result.faces(">Z")
    .workplane()
    .rect(slot_width, slot_length)
    .cutBlind(slot_depth)
)
