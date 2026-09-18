import cadquery as cq

# Parameters
plate_width = 100.0
plate_depth = 80.0
plate_thickness = 4.0
chamfer_size = 2.0
hole_diameter = 6.0
hole_pitch_x = 20.0
hole_pitch_y = 20.0
num_holes_x = 4
num_holes_y = 3
slot_length = 30.0
slot_width = 6.0
slot_spacing = 25.0
num_slots = 3
pocket_width = 30.0
pocket_depth = 15.0
pocket_depth_cut = 2.0

# Base plate with chamfered perimeter
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Central pocket cutout (non‑trivial feature)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_depth)
    .cutBlind(-pocket_depth_cut)
)

# Grid of through holes
result = (
    result
    .faces(">Z")
    .workplane()
    .rarray(hole_pitch_x, hole_pitch_y, num_holes_x, num_holes_y, True)
    .hole(hole_diameter)
)

# Linear array of slots for adjustable clamps
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, slot_spacing)
    .rarray(0, slot_spacing, 1, num_slots, True)
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
)
