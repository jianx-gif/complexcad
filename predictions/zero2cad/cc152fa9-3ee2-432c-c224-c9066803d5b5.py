import cadquery as cq

# Parameters
arm_length = 80.0
base_radius = 12.0
tip_radius = 6.0
fillet_radius = 2.0
hole_diameter = 4.0
hole_depth = 10.0
hole_spacing = 15.0
hole_count = 4
hole_start = 20.0
boss_radius = 15.0
boss_height = 5.0
pocket_width = 20.0
pocket_depth = 8.0
pocket_offset = 30.0

# Base profile for revolve (YZ plane)
profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(0, base_radius)
    .lineTo(arm_length * 0.6, base_radius)
    .lineTo(arm_length * 0.8, tip_radius)
    .lineTo(arm_length, tip_radius)
    .lineTo(arm_length, 0)
    .close()
)

# Revolve to create the arm
arm = profile.revolve()

# Fillet the tip edge (edges of the tip face)
arm = arm.faces(">X").edges().fillet(fillet_radius)

# Add a central boss at the base (cylinder along Y axis)
boss = (
    cq.Workplane("XZ")
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)
arm = arm.union(boss)

# Add a rectangular pocket on the side of the arm
pocket = (
    cq.Workplane("XZ")
    .center(pocket_offset, 0)
    .rect(pocket_width, pocket_depth)
    .extrude(base_radius * 2)
)
arm = arm.cut(pocket)

# Create blind holes pattern on the outer surface
for i in range(hole_count):
    x_pos = hole_start + i * hole_spacing
    hole = (
        cq.Workplane("XZ")
        .center(x_pos, 0)
        .circle(hole_diameter / 2)
        .extrude(-hole_depth)
    )
    arm = arm.cut(hole)

result = arm