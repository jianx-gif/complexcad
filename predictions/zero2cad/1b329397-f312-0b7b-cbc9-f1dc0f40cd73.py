import cadquery as cq

# Parameters
gear_outer_radius = 40.0
gear_thickness = 12.0
num_teeth = 12
tooth_width = 6.0
tooth_height = 6.0
tooth_overlap = 0.5
keyway_width = 10.0
keyway_depth = 8.0
chamfer_size = 0.5

# Base cylinder
base = cq.Workplane('XY').circle(gear_outer_radius).extrude(gear_thickness)

# Single tooth solid positioned with slight overlap into base
single_tooth = (
    cq.Workplane('XY')
    .rect(tooth_width, tooth_height)
    .extrude(gear_thickness)
    .translate((gear_outer_radius - tooth_overlap + tooth_width/2, 0, 0))
)

# Assemble teeth around the gear
gear = base
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    rotated_tooth = single_tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    gear = gear.union(rotated_tooth)

# Chamfer outer cylindrical edge
gear = gear.edges('|Z').chamfer(chamfer_size)

# Keyway cut (rectangular slot through the gear)
keyway = (
    cq.Workplane('XY')
    .box(keyway_depth, keyway_width, gear_thickness)
    .translate((gear_outer_radius - keyway_depth/2, 0, 0))
)

result = gear.cut(keyway)
