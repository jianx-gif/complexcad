import cadquery as cq
import math

# Parameters
bellows_length = 60.0
inner_radius = 20.0
wall_thickness = 5.0
corrugation_amplitude = 4.0
corrugation_count = 6
flange_thickness = 6.0
flange_radius = 35.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_count = 6
hole_offset = 2.0

# Derived dimensions
outer_radius = inner_radius + wall_thickness
segment_len = bellows_length / (corrugation_count * 2)

# Build bellows profile points (XZ plane)
points = []
points.append((0, 0))
points.append((inner_radius, 0))
for i in range(1, corrugation_count * 2 + 1):
    z = i * segment_len
    radius = inner_radius + (corrugation_amplitude if i % 2 == 1 else 0)
    points.append((radius, z))
points.append((0, bellows_length))

# Create bellows solid by revolving profile
bellows = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()
)

# Create flange solid and position it on top of bellows
flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
    .translate((0, 0, bellows_length))
)

# Union bellows and flange
result = bellows.union(flange)

# Apply chamfer to all edges for safety
result = result.edges().chamfer(chamfer_size)

# Add mounting holes on flange top face
hole_radius = flange_radius - hole_offset
hole_positions = []
for i in range(hole_count):
    angle = 2 * math.pi * i / hole_count
    x = hole_radius * math.cos(angle)
    y = hole_radius * math.sin(angle)
    hole_positions.append((x, y))

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
