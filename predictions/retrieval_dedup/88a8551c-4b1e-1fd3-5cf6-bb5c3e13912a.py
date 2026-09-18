import cadquery as cq
import math

# Parameters
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
spline_amplitude = 15.0
num_spline_points = 6
slot_width = 3.0
slot_length = 10.0
slot_spacing = 8.0
first_slot_offset = 12.0
num_slots = 5
mount_hole_diameter = 5.0
mount_hole_offset_x = 20.0
mount_hole_offset_y = 15.0

# Generate spline control points for top edge (sinusoidal variation)
spline_points = []
for i in range(num_spline_points):
    t = i / (num_spline_points - 1)
    x = plate_length * (1 - t)
    y = plate_width + spline_amplitude * math.sin(math.pi * t)
    spline_points.append((x, y))

# Base profile with spline edge on top
wp = cq.Workplane('XY')
profile = (
    wp
    .lineTo(plate_length, 0)
    .lineTo(plate_length, plate_width)
    .spline(spline_points)
    .close()
)

# Extrude base plate
solid = profile.extrude(plate_thickness)

# Mounting holes (cylindrical cut through)
hole_cutter = (
    cq.Workplane('XY')
    .pushPoints([
        (mount_hole_offset_x, mount_hole_offset_y),
        (plate_length - mount_hole_offset_x, mount_hole_offset_y)
    ])
    .circle(mount_hole_diameter / 2)
    .extrude(plate_thickness + 0.1)
)
solid = solid.cut(hole_cutter)

# Slots pattern within plate interior
slot_positions = []
for i in range(num_slots):
    x = first_slot_offset + i * slot_spacing
    y = plate_width / 2
    slot_positions.append((x, y))

slots = (
    cq.Workplane('XY')
    .pushPoints(slot_positions)
    .rect(slot_width, slot_length)
    .extrude(plate_thickness + 0.1)
)
solid = solid.cut(slots)

result = solid
