import cadquery as cq

flange_length = 60.0
flange_width = 30.0
flange_thickness = 8.0
vertical_leg_height = 40.0
pocket_width = 6.0
pocket_length = 30.0
pocket_depth = 4.0
hole_diameter = 6.0
countersink_diameter = 10.0
countersink_angle = 90.0
fillet_radius = 1.0
rib_width = 4.0
rib_spacing = 12.0
rib_depth = 2.0
hole_spacing = 20.0
hole_start_offset = flange_thickness + 12.0

# Base L‑shaped bracket profile
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (0, vertical_leg_height + flange_thickness),
        (flange_thickness, vertical_leg_height + flange_thickness),
        (flange_length, vertical_leg_height + flange_thickness),
        (flange_length, vertical_leg_height),
        (flange_thickness, vertical_leg_height),
        (flange_thickness, 0),
        (0, 0),
    ])
    .close()
    .extrude(flange_thickness)
)

# Recessed pocket in vertical leg
pocket_center_x = flange_thickness / 2.0
pocket_center_y = vertical_leg_height / 2.0
result = (
    base
    .faces(">Z")
    .workplane()
    .center(pocket_center_x, pocket_center_y)
    .rect(pocket_width, pocket_length)
    .cutBlind(pocket_depth)
)

# Countersunk M6 holes on horizontal flange
hole_positions = []
for i in range(3):
    x = hole_start_offset + i * hole_spacing
    y = flange_thickness / 2.0
    hole_positions.append((x, y))
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, flange_thickness)
)

# Lightening slots along horizontal leg
slot_positions = []
slot_start = flange_thickness + 10.0
slot_end = flange_length - 10.0
x = slot_start
while x <= slot_end:
    slot_positions.append((x, vertical_leg_height + flange_thickness / 2.0))
    x += rib_spacing
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(slot_positions)
    .rect(rib_width, flange_thickness * 0.6)
    .cutBlind(rib_depth)
)

# Apply uniform fillet for safety
result = result.fillet(fillet_radius)
