import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 20.0
height = 40.0
wall_thickness = 3.0
fillet_radius = 2.0
hole_diameter = 4.0
hole_count = 6
hole_pattern_radius = (inner_radius + outer_radius) / 2.0

# Build 2D profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .threePointArc((inner_radius - 5, height - 5), (inner_radius, 0))
    .close()
)

# Revolve profile around Z axis to create solid
solid = profile.revolve()

# Shell to create thin-walled bracket
hollow = solid.shell(wall_thickness)

# Fillet all edges for safety
filleted = hollow.edges().fillet(fillet_radius)

# Add patterned through holes on the top face
result = (
    filleted
    .faces(">Z")
    .workplane()
    .polarArray(0, 0, hole_pattern_radius, hole_count)
    .hole(hole_diameter)
)
