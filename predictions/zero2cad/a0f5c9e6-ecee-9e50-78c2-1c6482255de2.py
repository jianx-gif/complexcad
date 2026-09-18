import cadquery as cq

# Parameters
outer_radius = 45.0
inner_radius = 30.0
flange_thickness = 10.0
boss_radius = 12.0
boss_height = 15.0
fillet_radius = 2.0
hole_diameter = 5.0
hole_count = 6
hole_circle_radius = 35.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(boss_radius, 0)
    .lineTo(boss_radius, boss_height)
    .lineTo(inner_radius, boss_height)
    .lineTo(outer_radius, flange_thickness)
    .lineTo(outer_radius, 0)
    .close()
)

# Revolve profile around Z axis to create flange
flange = profile.revolve()

# Apply fillet to all edges for safety
flange = flange.edges().fillet(fillet_radius)

# Create patterned holes on top face
result = (
    flange
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_circle_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter)
)
