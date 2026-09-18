
import cadquery as cq

# Parameters
arm_length = 80.0
mount_height = 12.0
mount_radius = 30.0
base_radius = 20.0
taper_start_z = mount_height + 20.0
tip_radius = 3.0
fillet_radius = 2.0
hole_z = mount_height + 5.0
fastener_diameter = 5.0
countersink_diameter = 10.0
countersink_angle = 82.0
boss_radius = 6.0
boss_height = 10.0

# Base profile sketch on XZ plane
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(mount_radius, 0)
    .lineTo(mount_radius, mount_height)
    .lineTo(base_radius, mount_height)
    .lineTo(base_radius, taper_start_z)
    .lineTo(tip_radius, arm_length)
    .lineTo(0, arm_length)
    .close()
)

# Revolve to create the arm
arm = profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Add central boss for pivot
arm = (
    arm
    .faces("<Z")
    .workplane()
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_height)
    .union()
)

# Apply fillet to all edges
arm = arm.edges().fillet(fillet_radius)

# Create countersunk hole on side surface
arm = (
    arm
    .workplane(offset=0)
    .transformed(offset=(0, 0, hole_z), rotate=(0, 90, 0))
    .center(base_radius, 0)
    .cskHole(fastener_diameter, countersink_diameter, countersink_angle, depth=None)
)

result = arm
