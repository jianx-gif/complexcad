import cadquery as cq

# Parameters
inner_radius = 20.0
outer_radius = 30.0
bellows_length = 80.0
num_convolutions = 5
convolution_height = bellows_length / num_convolutions
wall_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_depth = wall_thickness + 0.5
hole_count = 8
hole_z = bellows_length * 0.5

# Build outer profile points for revolve
points = []
points.append((inner_radius, 0.0))
points.append((inner_radius, bellows_length))
points.append((outer_radius, bellows_length))
for i in range(num_convolutions):
    z_mid = bellows_length - (i + 0.5) * convolution_height
    points.append((outer_radius + 5.0, z_mid))
    z_next = bellows_length - (i + 1) * convolution_height
    points.append((outer_radius, z_next))
points.append((inner_radius, 0.0))

# Create solid by revolving profile
profile = cq.Workplane("XZ").polyline(points).close()
solid = profile.revolve()

# Shell to create thin wall
hollow = solid.shell(-wall_thickness)

# Chamfer top and bottom edges
hollow = hollow.faces(">Z").edges().chamfer(chamfer_size)
hollow = hollow.faces("<Z").edges().chamfer(chamfer_size)

# Add blind holes around circumference at mid-height
result = hollow
for i in range(hole_count):
    angle = i * 360.0 / hole_count
    hole = (
        cq.Workplane("YZ")
        .center(outer_radius - wall_thickness / 2.0, hole_z)
        .circle(hole_diameter / 2.0)
        .extrude(-hole_depth)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.cut(hole)
