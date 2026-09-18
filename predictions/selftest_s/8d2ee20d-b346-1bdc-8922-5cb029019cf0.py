import cadquery as cq
import math

gear_outer_radius = 50.0
gear_inner_radius = 30.0
gear_thickness = 15.0
pinion_radius = 20.0
pinion_height = 5.0
num_teeth = 20
tooth_height = 5.0
chamfer_size = 0.5
hole_diameter = 5.0
num_holes = 4
hole_pattern_radius = gear_inner_radius * 0.5

# Base gear cylinder
base = cq.Workplane('XY').circle(gear_outer_radius).extrude(gear_thickness)
# Raised pinion on top
pinion = cq.Workplane('XY').circle(pinion_radius).extrude(pinion_height).translate((0, 0, gear_thickness))
combined = base.union(pinion)
# Mounting holes through hub
hole_positions = []
angle_step = 360 / num_holes
for i in range(num_holes):
    ang = math.radians(i * angle_step)
    x = hole_pattern_radius * math.cos(ang)
    y = hole_pattern_radius * math.sin(ang)
    hole_positions.append((x, y))
combined = combined.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter, depth=gear_thickness + pinion_height)
# Tooth profile
tooth_pitch = 2 * math.pi / num_teeth
tooth_width = 2 * gear_outer_radius * math.sin(tooth_pitch / 2) * 0.8
# Create single tooth solid for cutting
single_tooth = (cq.Workplane('XY')
    .center(gear_outer_radius - tooth_height / 2, 0)
    .rect(tooth_width, tooth_height)
    .extrude(gear_thickness + pinion_height))
# Cut teeth around circumference
gear_with_teeth = combined
for i in range(num_teeth):
    angle_deg = i * 360 / num_teeth
    tooth_copy = single_tooth.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    gear_with_teeth = gear_with_teeth.cut(tooth_copy)
# Chamfer outer edges of teeth
result = gear_with_teeth.edges('>Z').chamfer(chamfer_size)
