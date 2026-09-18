import cadquery as cq
import math

# Parameters
base_radius = 30.0
top_radius = 15.0
gear_height = 40.0
num_teeth = 20
tooth_depth = 5.0
pitch = 2 * math.pi * base_radius / num_teeth
tooth_width = 0.6 * pitch
hole_diameter = 8.0
fillet_radius = 0.5

# Base cone (bevel gear blank)
cone = cq.Workplane('XY').add(cq.Solid.makeCone(base_radius, top_radius, gear_height))

# Tooth cut block (rectangular prism intersecting cone)
tooth_block = (
    cq.Workplane('XY')
    .center(base_radius + tooth_depth / 2.0, 0)
    .rect(tooth_depth, tooth_width)
    .extrude(gear_height)
)

# Subtract teeth by rotating the block around Z axis
gear = cone
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    gear = gear.cut(tooth_block.rotate((0, 0, 0), (0, 0, 1), angle))

# Central mounting hole through top face
gear = gear.faces('>Z').workplane().hole(hole_diameter)

# Fillet on all edges for safety
gear = gear.edges().fillet(fillet_radius)

result = gear