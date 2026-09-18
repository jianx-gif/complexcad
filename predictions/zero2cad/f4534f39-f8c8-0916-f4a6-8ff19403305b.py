import cadquery as cq
import math

# Parameters
flange_radius = 30.0
flange_thickness = 8.0
body_radius = 12.0
body_length = 30.0
neck_radius = 6.0
neck_length = 20.0
fillet_radius = 2.0
central_hole_diameter = 8.0
mount_hole_diameter = 4.0
mount_hole_count = 4
mount_hole_radius = 20.0
pocket_width = 10.0
pocket_height = 6.0
pocket_depth = 4.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(flange_radius, 0)
    .lineTo(flange_radius, flange_thickness)
    .lineTo(body_radius, flange_thickness)
    .lineTo(body_radius, flange_thickness + body_length)
    .lineTo(neck_radius, flange_thickness + body_length)
    .lineTo(neck_radius, flange_thickness + body_length + neck_length)
    .lineTo(0, flange_thickness + body_length + neck_length)
    .close()
)

# Revolve to create solid
solid = profile.revolve()

# Fillet all edges for smooth transition
solid = solid.edges().fillet(fillet_radius)

# Central through hole
solid = solid.faces(">Z").workplane().hole(central_hole_diameter)

# Mounting holes on flange (bottom face)
mount_points = [
    (
        mount_hole_radius * math.cos(2 * math.pi * i / mount_hole_count),
        mount_hole_radius * math.sin(2 * math.pi * i / mount_hole_count),
    )
    for i in range(mount_hole_count)
]
solid = solid.faces("<Z").workplane().pushPoints(mount_points).hole(mount_hole_diameter)

# Pocket on side of body for weight reduction
solid = (
    solid.faces(">Z")
    .workplane(offset=flange_thickness + body_length / 2)
    .rect(pocket_width, pocket_height)
    .cutBlind(pocket_depth)
)

result = solid