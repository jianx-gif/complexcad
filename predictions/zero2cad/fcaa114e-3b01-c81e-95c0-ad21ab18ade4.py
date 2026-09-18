import cadquery as cq

# Parameters
outer_radius = 40.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
channel_length = 60.0
lip_height = 10.0
lip_extension = 5.0
fillet_radius = 0.5
hole_diameter = 4.0
hole_count = 12
hole_depth = wall_thickness + 0.5

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, channel_length)
    .lineTo(outer_radius, channel_length + lip_height)
    .lineTo(outer_radius + lip_extension, channel_length)
    .lineTo(outer_radius + lip_extension, 0)
    .close()
)

# Revolve to create thin-walled channel with lip
solid = profile.revolve()

# Fillet all edges for safety
solid = solid.edges().fillet(fillet_radius)

# Create radial holes around the outer wall
result = solid
for i in range(hole_count):
    angle = i * 360.0 / hole_count
    hole = (
        cq.Workplane("XY")
        .center(outer_radius - wall_thickness/2, 0)
        .circle(hole_diameter/2)
        .extrude(hole_depth)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.cut(hole)
