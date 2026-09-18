import cadquery as cq
import math

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
perimeter_fillet = 4.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_width = 12.0
rib_height = 2.5
hex_side = 5.0
hex_rows = 5
hex_cols = 6
hex_spacing_x = hex_side * 2.5
hex_spacing_y = hex_side * 2.2
hex_offset_x = perimeter_fillet + hex_side * 1.5
hex_offset_y = perimeter_fillet + hex_side * 1.5
hex_diameter = hex_side * 2.0

# Base plate
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)
base = base.edges("|Z").fillet(perimeter_fillet)

# Mounting holes at four corners
half_len = plate_length / 2.0
half_wid = plate_width / 2.0
off = mount_hole_offset
mount_pts = [( half_len - off,  half_wid - off),
             (-half_len + off,  half_wid - off),
             (-half_len + off, -half_wid + off),
             ( half_len - off, -half_wid + off)]
base = base.faces(">Z").workplane().pushPoints(mount_pts).hole(mount_hole_diameter)

# Structural ribs on top surface
rib1 = cq.Workplane("XY").box(rib_width, plate_length, rib_height).translate((0, 0, plate_thickness/2 + rib_height/2))
rib2 = cq.Workplane("XY").box(plate_length, rib_width, rib_height).translate((0, 0, plate_thickness/2 + rib_height/2))
base = base.union(rib1).union(rib2)

# Hexagonal cutout grid
points = []
for i in range(hex_cols):
    for j in range(hex_rows):
        x = -half_len + hex_offset_x + i * hex_spacing_x
        y = -half_wid + hex_offset_y + j * hex_spacing_y
        if (abs(x) + hex_side) < (half_len - perimeter_fillet) and (abs(y) + hex_side) < (half_wid - perimeter_fillet):
            points.append((x, y))

base = base.faces("<Z").workplane().pushPoints(points).polygon(6, hex_diameter).cutBlind(-plate_thickness)

result = base