import cadquery as cq
import math

# Parameters
gear_outer_radius = 45.0
gear_inner_radius = 15.0
gear_thickness = 12.0
tooth_count = 24
tooth_depth = 5.0
tooth_width = (2 * math.pi * gear_outer_radius) / tooth_count * 0.6
chamfer_size = 1.0
boss_radius = 5.0
boss_height = 6.0
boss_offset = gear_inner_radius + 5.0

# Base ring
base_ring = (
    cq.Workplane("XY")
    .circle(gear_outer_radius)
    .circle(gear_inner_radius)
    .extrude(gear_thickness)
)

# Central boss
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((boss_offset, 0, gear_thickness))
)

# Combine base and boss
combined = base_ring.union(boss)

# Chamfer all edges for safety
combined = combined.edges().chamfer(chamfer_size)

# Tooth profile (single tooth)
single_tooth = (
    cq.Workplane("XY")
    .center(gear_outer_radius - tooth_depth / 2, 0)
    .rect(tooth_width, gear_thickness)
    .extrude(gear_thickness)
)

# Add teeth around the gear
result = combined
for i in range(tooth_count):
    angle = i * 360.0 / tooth_count
    rotated_tooth = single_tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_tooth)
