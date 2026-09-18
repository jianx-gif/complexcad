import cadquery as cq

# Parameters
arm_length = 80.0
arm_outer_radius = 8.0
arm_inner_radius = 5.0
rib_start = 30.0
rib_end = 50.0
rib_thickness = 1.5
tip_radius = 4.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_offset = 12.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(arm_inner_radius, 0)
    .lineTo(arm_outer_radius, 0)
    .lineTo(arm_outer_radius, rib_start)
    .lineTo(arm_outer_radius + rib_thickness, rib_start)
    .lineTo(arm_outer_radius + rib_thickness, rib_end)
    .lineTo(arm_outer_radius, rib_end)
    .lineTo(arm_outer_radius, arm_length - tip_radius)
    .threePointArc((arm_outer_radius + tip_radius, arm_length - tip_radius/2), (arm_outer_radius + tip_radius, arm_length))
    .lineTo(arm_inner_radius, arm_length)
    .close()
)

# Revolve to create arm
arm = profile.revolve()

# Chamfer base edge
arm = arm.faces("<Z").edges().chamfer(chamfer_size)

# Add mounting holes on base face
arm = (
    arm.faces("<Z")
    .workplane()
    .pushPoints([(-hole_offset, 0), (hole_offset, 0)])
    .hole(hole_diameter)
)

result = arm