import cadquery as cq

# Parameters
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 6.0
rib_width = 8.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 5
hole_diameter = 5.0
hole_depth = 4.0
hole_pitch_x = 20.0
hole_pitch_y = 20.0
hole_rows = 3
hole_cols = 4
slot_width = 6.0
slot_length = 40.0
slot_depth = 3.0
chamfer_size = 0.8

# Base plate
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)

# Ribbed back (extrude ribs on the -Z face)
ribs = (
    base.faces("<Z").workplane()
    .rect(rib_width, plate_depth)
    .rarray(rib_spacing, 0, rib_count, 1, True)
    .extrude(-rib_height)
)

# Combine base and ribs
combined = base.union(ribs)

# Blind holes on top face
holes = (
    combined.faces(">Z").workplane()
    .rarray(hole_pitch_x, hole_pitch_y, hole_cols, hole_rows, True)
    .circle(hole_diameter / 2)
    .cutBlind(hole_depth)
)

# Central slot on top face
slot = (
    holes.faces(">Z").workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(slot_depth)
)

# Chamfer edges
result = (
    slot.edges("|Z").chamfer(chamfer_size)
)
