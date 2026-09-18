import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 30.0
arm_thickness = 10.0
boss_diameter = 20.0
boss_height = 15.0
fillet_radius = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
rib_width = 6.0
rib_height = 8.0
rib_offset = 5.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(boss_diameter / 2, 0)
    .lineTo(boss_diameter / 2, boss_height)
    .lineTo(arm_width / 2, boss_height)
    .lineTo(arm_width / 2, arm_length)
    .lineTo(0, arm_length)
    .close()
)

# Revolve to create the arm with central boss
arm = profile.revolve()

# Fillet all edges for safety
arm = arm.edges().fillet(fillet_radius)

# Add two symmetric through holes on the top face
arm = (
    arm.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .hole(hole_diameter)
)

# Add a reinforcing rib on the outer side of the arm
rib = (
    cq.Workplane("XY")
    .center(-arm_width / 2 + rib_offset, 0)
    .rect(rib_width, rib_height)
    .extrude(arm_length)
)

result = arm.union(rib)
