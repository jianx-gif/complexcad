import cadquery as cq

# Parameters
gear_module = 1.5
num_teeth = 42
pitch_diameter = gear_module * num_teeth
base_radius = pitch_diameter / 2.0
addendum = gear_module
dedendum = 1.25 * gear_module
outer_radius = base_radius + addendum
gear_thickness = 10.0
tooth_width = (3.14159 * pitch_diameter) / (2 * num_teeth) * 0.8
tooth_depth = addendum + dedendum
vent_diameter = 5.0
vent_center_radius = outer_radius - 8.0
chamfer_size = 0.8

# Base cylinder
base = cq.Workplane('XY').circle(base_radius).extrude(gear_thickness)

# Single tooth profile placed to intersect base
tooth = (cq.Workplane('XY')
    .center(base_radius - tooth_depth/2.0, 0)
    .rect(tooth_width, tooth_depth)
    .extrude(gear_thickness)
)

# Assemble teeth by rotation and union with base
gear = base
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    tooth_copy = tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    gear = gear.union(tooth_copy)

# Add rust-prevention vents through the gear
gear = (gear.faces('>Z')
    .workplane()
    .polarArray(count=8, radius=vent_center_radius, startAngle=0, angle=360)
    .hole(vent_diameter)
)

# Chamfer all edges
gear = gear.edges().chamfer(chamfer_size)

result = gear