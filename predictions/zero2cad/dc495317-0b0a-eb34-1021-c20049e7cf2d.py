import cadquery as cq

# Parameters
arm_length = 80.0
base_radius = 15.0
step_radius = 10.0
step_position = 40.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 6.0
hole_depth = 12.0
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0
mount_hole_offset = 10.0

# Base profile for revolve (XY plane, revolve about Z)
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, step_position)
    .lineTo(step_radius, step_position)
    .lineTo(step_radius, arm_length)
    .lineTo(0, arm_length)
    .close()
)

# Revolve to create solid arm
solid_arm = profile.revolve()

# Shell to create hollow interior
hollow_arm = solid_arm.shell(-wall_thickness)

# Chamfer outer edges for safety
chamfered_arm = hollow_arm.edges().chamfer(chamfer_size)

# Blind tapped hole at the base (centered on axis)
arm_with_hole = (
    chamfered_arm
    .faces("<Z")
    .workplane()
    .hole(hole_diameter, depth=hole_depth)
)

# Mounting holes on the base face, arranged in a square pattern
mount_points = [
    ( mount_hole_offset,  mount_hole_offset),
    (-mount_hole_offset,  mount_hole_offset),
    (-mount_hole_offset, -mount_hole_offset),
    ( mount_hole_offset, -mount_hole_offset),
]
result = (
    arm_with_hole
    .faces("<Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)
