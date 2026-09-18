import cadquery as cq
import math

# Parameters
outer_radius = 40.0
inner_radius = 20.0
block_height = 50.0
shoulder_height = 15.0
fillet_radius = 2.0
hole_diameter = 5.5
hole_count = 6
hole_circle_radius = 30.0
rib_thickness = 4.0
rib_height = 30.0
rib_offset = 5.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, block_height - shoulder_height)
    .threePointArc((outer_radius - fillet_radius, block_height - shoulder_height + fillet_radius), (inner_radius, block_height - shoulder_height))
    .lineTo(inner_radius, block_height)
    .lineTo(0, block_height)
    .close()
)

# Revolve to create axisymmetric block
solid = profile.revolve()

# Fillet the outer top edge (horizontal edge at top)
solid = solid.edges(">Z").fillet(fillet_radius)

# Add a reinforcing rib on the outer cylindrical surface
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_offset, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)

# Create six M5 clearance holes on the top face
hole_positions = [
    (
        hole_circle_radius * math.cos(2 * math.pi * i / hole_count),
        hole_circle_radius * math.sin(2 * math.pi * i / hole_count)
    )
    for i in range(hole_count)
]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

result = solid