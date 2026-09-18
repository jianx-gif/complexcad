import cadquery as cq
import math

# Parameter definitions
height = 80.0
base_outer_radius = 30.0
base_inner_radius = 20.0
taper_end_radius = 15.0
wall_thickness = 2.0
num_bellows = 5
wave_amplitude = 5.0
notch_depth = 2.0
notch_position_height = 10.0
notch_height = 4.0
chamfer_size = 1.0
vent_hole_radius = 2.0
vent_rows = 3
vent_per_row = 8
edge_margin = 5.0

# Derived dimensions
bellows_section_height = height - 10.0  # taper height = 10.0
half_wave_height = bellows_section_height / (num_bellows * 2)

# Build profile points (XZ plane, revolve about Y)
points = []
points.append((base_inner_radius, 0.0))
points.append((base_outer_radius, 0.0))
points.append((base_outer_radius - notch_depth, notch_position_height))
points.append((base_outer_radius, notch_position_height + notch_height))
current_y = notch_position_height + notch_height
for i in range(num_bellows * 2):
    r = base_outer_radius + wave_amplitude if i % 2 == 0 else base_outer_radius
    current_y += half_wave_height
    points.append((r, current_y))
points.append((taper_end_radius, height))
points.append((base_inner_radius, height))

# Create the revolved solid
profile = cq.Workplane("XZ")
for idx, (x, y) in enumerate(points):
    if idx == 0:
        profile = profile.moveTo(x, y)
    else:
        profile = profile.lineTo(x, y)
solid = profile.close().revolve()

# Shell to create hollow bellows
hollow = solid.shell(-wall_thickness)

# Add vent holes using radial cylinders
result = hollow
for row in range(vent_rows):
    z_offset = edge_margin + row * ((height - 2 * edge_margin) / (vent_rows - 1))
    for n in range(vent_per_row):
        angle = 2 * math.pi * n / vent_per_row
        radial = base_outer_radius + wave_amplitude / 2
        y_pos = radial * math.sin(angle)
        vent = (
            cq.Workplane("YZ")
            .center(y_pos, z_offset)
            .circle(vent_hole_radius)
            .extrude(wall_thickness * 2 + 2)
        )
        result = result.cut(vent)

# Chamfer bottom and top outer edges for safety
bottom_chamfer = result.faces("<Z").edges().chamfer(chamfer_size)
result = bottom_chamfer.faces(">Z").edges().chamfer(chamfer_size)
