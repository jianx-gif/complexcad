import cadquery as cq

# Parameters
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
cap_height = 20.0
lip_height = 2.0
lip_extension = 3.0
fillet_radius = 0.5
vent_hole_diameter = 2.0
vent_hole_count = 12
vent_hole_radius = (inner_radius + outer_radius) / 2.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, cap_height - lip_height)
    .lineTo(outer_radius, cap_height - lip_height)
    .lineTo(outer_radius + lip_extension, cap_height - lip_height)
    .lineTo(outer_radius + lip_extension, cap_height)
    .lineTo(outer_radius, cap_height)
    .lineTo(inner_radius, cap_height)
    .close()
)

# Revolve to create cap
result = profile.revolve()

# Fillet all edges for safety
result = result.edges().fillet(fillet_radius)

# Add vent holes on top face
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=vent_hole_radius, count=vent_hole_count, startAngle=0, angle=360)
    .hole(vent_hole_diameter)
)
