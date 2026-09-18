import cadquery as cq
import math

# Parameters
gear_diameter = 60.0
gear_length = 30.0
num_teeth = 20
tooth_height = 5.0
tooth_width = 6.0
keyway_width = 8.0
keyway_depth = 4.0
chamfer_size = 0.8

# Derived dimensions
base_radius = gear_diameter / 2.0
tooth_center_radius = base_radius + tooth_height / 2.0

# Base cylinder (gear body without teeth)
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(gear_length)
)

# Single tooth solid positioned at 0 degrees
single_tooth = (
    cq.Workplane("XY")
    .center(tooth_center_radius, 0)
    .rect(tooth_width, tooth_height)
    .extrude(gear_length)
)

# Assemble gear by rotating and unioning teeth
gear = base
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    rotated_tooth = single_tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    gear = gear.union(rotated_tooth)

# Keyway cut (rectangular slot through the gear length)
keyway = (
    cq.Workplane("XY")
    .center(base_radius / 2.0, 0)
    .rect(keyway_depth, keyway_width)
    .extrude(gear_length)
)

# Apply keyway cut
gear = gear.cut(keyway)

# Chamfer outer cylindrical edge for safety
gear = gear.edges("|Z").chamfer(chamfer_size)

result = gear