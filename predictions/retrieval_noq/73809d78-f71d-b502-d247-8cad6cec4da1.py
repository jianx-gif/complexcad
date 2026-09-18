import cadquery as cq

# Dimensions (max 100 units)
handle_length = 80.0
handle_width = 30.0
handle_height = 20.0
wall_thickness = 2.0
hole_diameter = 8.0
fillet_radius = 1.5

# Create ergonomic 2D profile (closed shape) in XY plane
profile = (
    cq.Workplane("XY")
    .moveTo(-handle_length/2, -handle_width/2)
    .lineTo(handle_length/2, -handle_width/2)
    .lineTo(handle_length/2, handle_width/4)
    .threePointArc((handle_length/2 - 5, handle_width/2), (0, handle_width/2))
    .threePointArc((-handle_length/2 + 5, handle_width/2), (-handle_length/2, handle_width/4))
    .lineTo(-handle_length/2, -handle_width/2)
    .close()
)

# Extrude to create solid grip
solid = profile.extrude(handle_height)

# Add central through-hole before shell
solid = solid.faces(">Z").workplane(centerOption="CenterOfMass").hole(hole_diameter)

# Shell to create hollow interior
hollow = solid.shell(-wall_thickness)

# Apply fillet to outer vertical edges
result = hollow.edges("|Z").fillet(fillet_radius)
