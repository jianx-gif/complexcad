import cadquery as cq

# Parameters
plate_length = 100.0
plate_width = 70.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 5.0
rib_spacing = 10.0
rib_margin = 10.0
slot_width = 10.0
slot_length = 30.0
slot_offset = 15.0
hole_diameter = 5.0
hole_spacing_x = 30.0
hole_spacing_y = 30.0
hole_rows = 2
hole_cols = 2
chamfer_size = 1.0

# Base plate with chamfered outer edges
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_length)
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Ribbed edge on top surface
rib_count = int((plate_width - 2 * rib_margin + rib_spacing) // (rib_width + rib_spacing))
rib_start = -plate_width / 2 + rib_margin + rib_width / 2
rib_positions = [rib_start + i * (rib_width + rib_spacing) for i in range(rib_count)]
rib_points = [(x, 0) for x in rib_positions]

ribs = (
    base.faces(">Z").workplane()
    .pushPoints(rib_points)
    .rect(rib_width, plate_thickness + rib_height)
    .extrude(rib_height)
)

# Combine base and ribs
combined = base.union(ribs)

# Side slot on -X face
slot = (
    combined.faces("<X").workplane()
    .center(0, slot_offset)
    .rect(slot_width, slot_length)
    .cutBlind(-plate_thickness)
)

# Mounting holes pattern on top surface
hole_start_x = -plate_width / 2 + hole_spacing_x / 2
hole_start_y = -plate_length / 2 + hole_spacing_y / 2
hole_points = []
for i in range(hole_cols):
    for j in range(hole_rows):
        x = hole_start_x + i * hole_spacing_x
        y = hole_start_y + j * hole_spacing_y
        hole_points.append((x, y))

result = (
    slot.faces(">Z").workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)
