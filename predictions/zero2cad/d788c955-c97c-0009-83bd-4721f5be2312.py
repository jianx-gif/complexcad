import cadquery as cq

# Parameters
leg_length = 60.0
leg_width = 30.0
thickness = 10.0
fillet_radius = 2.0
hole_diameter = 5.0
hole_depth = 8.0
hole_spacing = 12.0
hole_offset = 15.0

# L-shaped profile in YZ plane
profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(0, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length - thickness)
    .lineTo(thickness, leg_length - thickness)
    .lineTo(thickness, 0)
    .close()
)

# Revolve around Y axis to create bracket
bracket = profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Apply fillet to all edges for safety
bracket = bracket.edges().fillet(fillet_radius)

# Create blind holes on the outer cylindrical face
hole_positions = [(0, hole_offset + i * hole_spacing) for i in range(3)]
bracket = (
    bracket
    .faces(">X")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter / 2)
    .cutBlind(hole_depth)
)

result = bracket