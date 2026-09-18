import cadquery as cq
import math

# Parameters
gear_outer_radius = 45.0
gear_thickness = 12.0
hub_radius = 18.0
hub_height = 16.0
tooth_count = 20
tooth_depth = 5.0
tooth_width_factor = 0.6
chamfer_size = 0.5
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = hub_radius * 0.7

# Derived dimensions
tooth_width = (2 * math.pi * gear_outer_radius) / tooth_count * tooth_width_factor

# Base gear cylinder
gear_body = (
    cq.Workplane("XY")
    .circle(gear_outer_radius)
    .extrude(gear_thickness)
)

# Hub cylinder
hub = (
    cq.Workplane("XY")
    .circle(hub_radius)
    .extrude(hub_height)
)

# Combine gear and hub
combined = gear_body.union(hub)

# Tooth cut solid (single tooth)
single_tooth = (
    cq.Workplane("XY")
    .center(gear_outer_radius - tooth_depth / 2, 0)
    .rect(tooth_width, tooth_depth)
    .extrude(gear_thickness + 2)
)

# Cut teeth around the gear
for i in range(tooth_count):
    angle = i * 360.0 / tooth_count
    rotated_tooth = single_tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    combined = combined.cut(rotated_tooth)

# Add mounting holes on hub top face
combined = (
    combined
    .faces(">Z")
    .workplane()
    .polarArray(mount_hole_radius, 0, 360, mount_hole_count)
    .hole(mount_hole_diameter)
)

# Apply chamfer to top edges for safety
result = combined.faces(">Z").edges().chamfer(chamfer_size)
