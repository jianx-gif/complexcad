import cadquery as cq
import math

# Parameters
gear_outer_radius = 45.0
gear_inner_radius = 20.0
gear_thickness = 8.0
num_teeth = 28
tooth_depth = 4.0
tooth_width = (2 * math.pi * gear_inner_radius) / num_teeth * 0.6
chamfer_size = 0.4

# Base cylinder
base = cq.Workplane('XY').cylinder(gear_thickness, gear_outer_radius)

# Tooth solid (single tooth)
tooth = (
    cq.Workplane('XY')
    .rect(tooth_width, tooth_depth)
    .extrude(gear_thickness)
    .translate((gear_inner_radius + tooth_depth / 2.0, 0, 0))
)

# Cut teeth around inner circumference
gear = base
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    gear = gear.cut(tooth.rotate((0, 0, 0), (0, 0, 1), angle))

# Apply chamfer to all edges for safety
result = gear.edges().chamfer(chamfer_size)
