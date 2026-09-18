import cadquery as cq

# Parameters
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 2.0
channel_height = 20.0
fillet_radius = 1.0
hole_diameter = 4.0
hole_count = 8
hole_center_radius = (inner_radius + outer_radius) / 2.0
flange_thickness = 5.0
flange_radius = outer_radius + 5.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, channel_height)
    .threePointArc((outer_radius, channel_height + 5), (outer_radius, 0))
    .close()
)

# Revolve to create solid channel
solid = profile.revolve()

# Shell to create thin-walled channel
hollow = solid.shell(-wall_thickness)

# Fillet outer rim edges (top and bottom)
filleted = hollow.edges(">Z or <Z").fillet(fillet_radius)

# Add mounting flange on bottom face
flanged = (
    filleted
    .faces("<Z")
    .workplane()
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# Create radial holes pattern
holes = (
    cq.Workplane("XY")
    .polarArray(radius=hole_center_radius, startAngle=0, angle=360, count=hole_count)
    .circle(hole_diameter / 2)
    .extrude(wall_thickness * 2)
    .rotate((0, 0, 0), (0, 1, 0), 90)
)

# Cut holes through the wall
result = flanged.cut(holes)
