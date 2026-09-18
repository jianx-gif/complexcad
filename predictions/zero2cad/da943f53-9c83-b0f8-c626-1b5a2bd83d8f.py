import cadquery as cq

# Parameters
base_radius = 15.0
top_radius = 40.0
gear_height = 30.0
num_teeth = 20
tooth_width = 4.0
tooth_depth = 5.0
chamfer_size = 0.5
boss_radius = 6.0
boss_height = 5.0

# Base conical gear body
gear_body = (
    cq.Workplane("XY")
    .circle(base_radius)
    .workplane(offset=gear_height)
    .circle(top_radius)
    .loft()
)

# Single tooth cut solid positioned at outer radius
single_tooth = (
    cq.Workplane("XY")
    .rect(tooth_width, gear_height)
    .extrude(tooth_depth)
    .translate((top_radius - tooth_depth / 2, 0, 0))
)

# Apply tooth cuts around the gear
gear_with_teeth = gear_body
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    rotated_tooth = single_tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    gear_with_teeth = gear_with_teeth.cut(rotated_tooth)

# Chamfer all edges for safety
gear_chamfered = gear_with_teeth.edges().chamfer(chamfer_size)

# Add central boss on top face
result = (
    gear_chamfered
    .faces(">Z")
    .workplane()
    .circle(boss_radius)
    .extrude(boss_height)
)
