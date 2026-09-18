import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
fillet_radius = 3.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_rows = 4
hole_cols = 4
rib_height = 6.0
rib_thickness = 4.0
rib_offset = 30.0

# Base profile for revolve (YZ plane)
profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(0, arm_thickness)
    .lineTo(arm_length, arm_thickness)
    .threePointArc((arm_length + fillet_radius, arm_thickness / 2), (arm_length, 0))
    .close()
)

# Revolve to create the arm
arm = profile.revolve()

# Add a reinforcing rib on the outer surface
rib = (
    arm.faces(">Z")
    .workplane()
    .center(rib_offset, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
)
arm = arm.union(rib)

# Patterned through holes on the top face
arm = (
    arm.faces(">Z")
    .workplane()
    .rarray(hole_spacing, hole_spacing, hole_cols, hole_rows)
    .hole(hole_diameter)
)

result = arm