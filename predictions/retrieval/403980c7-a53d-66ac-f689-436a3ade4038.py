import cadquery as cq
import math

# Parameters
gear_height = 30.0
cone_full_angle = 60.0
taper_angle = -cone_full_angle / 2  # degrees, negative expands radius upward
root_radius = 20.0
tooth_count = 16
tooth_width = 4.0
tooth_thickness = 6.0
tooth_height = gear_height * 0.9
tooth_depth = 2.0

dowel_diameter = 3.0
dowel_count = 4
dowel_radius = 12.0
central_shaft_diameter = 6.0
chamfer_dist = 0.5

# Base conical gear body
base_gear = (
    cq.Workplane('XY')
    .circle(root_radius)
    .extrude(gear_height, taper=taper_angle)
)

# Outer radius at top after taper
outer_radius = root_radius + gear_height * math.tan(math.radians(-taper_angle))
mid_z = gear_height / 2

# Template tooth positioned at 0 degrees
template_tooth = (
    cq.Workplane('XY')
    .rect(tooth_width, tooth_thickness)
    .extrude(tooth_height)
    .translate((outer_radius + tooth_depth/2, 0, mid_z - tooth_height/2))
)

# Assemble teeth by rotating the template around Z axis
gear_with_teeth = base_gear
for i in range(tooth_count):
    angle_deg = i * 360.0 / tooth_count
    rotated_tooth = template_tooth.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    gear_with_teeth = gear_with_teeth.union(rotated_tooth)

# Dowel pin holes pattern on top face
gear_with_dowels = (
    gear_with_teeth
    .faces('>Z')
    .workplane()
    .circle(dowel_radius)
    .polarArray(radius=dowel_radius, startAngle=0, count=dowel_count, angle=360)
    .hole(dowel_diameter)
)

# Central shaft bore through bottom face
gear_with_shaft = (
    gear_with_dowels
    .faces('<Z')
    .workplane()
    .hole(central_shaft_diameter)
)

# Chamfer edges for safety
result = (
    gear_with_shaft
    .edges('>Z')
    .chamfer(chamfer_dist)
)
