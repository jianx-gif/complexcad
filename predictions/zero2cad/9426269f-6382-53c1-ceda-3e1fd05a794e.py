import cadquery as cq

# Parameters
plate_width = 90.0
plate_depth = 60.0
plate_thickness = 4.0
split_gap = 2.0
hole_diameter = 4.0
hole_radius = hole_diameter / 2.0
hole_pitch_x = 30.0
hole_pitch_y = 20.0
hole_rows = 2
hole_cols = 3
chamfer_size = 0.5

# Base plate
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)

# Split slot (central narrow cut)
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(split_gap, plate_depth)
    .extrude(plate_thickness + 0.1)
)

# Apply split slot cut
plate_with_slot = base.cut(slot)

# Add six through holes (2 rows x 3 columns)
holes = (
    plate_with_slot
    .faces(">Z")
    .workplane()
    .center(-hole_pitch_x, -hole_pitch_y/2)
    .rarray(hole_pitch_x, hole_pitch_y, hole_cols, hole_rows, True)
    .hole(hole_diameter)
)

# Apply chamfer to vertical edges
result = (
    holes
    .edges("|Z")
    .chamfer(chamfer_size)
)
