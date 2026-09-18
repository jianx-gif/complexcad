import cadquery as cq

# Parameters
outer_radius = 30.0
base_height = 12.0
shoulder_radius = 20.0
shoulder_height = 5.0
top_radius = 8.0
top_height = 10.0
fillet_radius = 1.5
hole_diameter = 4.5
hole_offset = 12.0

# Build profile for revolve
profile = (
    cq.Workplane("YZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, base_height)
    .lineTo(shoulder_radius, base_height)
    .lineTo(shoulder_radius, base_height + shoulder_height)
    .lineTo(top_radius, base_height + shoulder_height + top_height)
    .lineTo(0, base_height + shoulder_height + top_height)
    .close()
)

# Revolve profile around Z axis
solid = profile.revolve()

# Apply fillet to all edges for safety
solid = solid.edges().fillet(fillet_radius)

# Add four M4 clearance holes on the top face
result = (
    solid
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_offset, 0),
        (-hole_offset, 0),
        (0, hole_offset),
        (0, -hole_offset),
    ])
    .hole(hole_diameter)
)
