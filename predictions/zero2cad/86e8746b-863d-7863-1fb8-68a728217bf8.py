import cadquery as cq

# Parameters
arm_length = 80.0
arm_thickness = 12.0
boss_radius = 10.0
boss_height = 15.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_depth = 8.0
hole_spacing = 12.0
num_holes = 5
hole_start_offset = 20.0

# Base profile for revolve (XY plane, revolve about Z)
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(boss_height, boss_radius)
    .lineTo(arm_length, arm_thickness)
    .lineTo(arm_length, 0)
    .close()
)

# Revolve to create the pivot arm
result = profile.revolve()

# Chamfer outer edge (all edges for simplicity)
result = result.edges().chamfer(chamfer_size)

# Create blind holes on the top face (Z+)
# Determine hole positions along X axis
hole_positions = []
for i in range(num_holes):
    x = hole_start_offset + i * hole_spacing
    if x > arm_length - hole_start_offset:
        break
    hole_positions.append((x, 0))

# Drill blind holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, depth=hole_depth)
)
