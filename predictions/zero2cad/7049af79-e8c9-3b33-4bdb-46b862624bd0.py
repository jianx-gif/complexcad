import cadquery as cq

# Parameters
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 5.0
corner_fillet_radius = 5.0
hole_diameter = 8.0
hole_spacing = 20.0
hole_count = 3
slot_length = 30.0
slot_width = 6.0
slot_offset_from_edge = 10.0
chamfer_size = 0.8

# Base plate with a filleted corner (top‑right)
base = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .edges("|Z and >X and >Y")
    .fillet(corner_fillet_radius)
)

# Add a row of through holes centered on the plate
holes = (
    base
    .faces(">Z")
    .workplane()
    .center(-((hole_count - 1) * hole_spacing) / 2, 0)
    .rarray(hole_spacing, 0, hole_count, 1, True)
    .hole(hole_diameter)
)

# Add a side slot for a latch on the +X face
slot = (
    holes
    .faces(">X")
    .workplane()
    .center(0, -plate_depth / 2 + slot_offset_from_edge + slot_width / 2)
    .slot2D(slot_length, slot_width, 0)
    .cutBlind(-plate_thickness)
)

# Apply a small chamfer to all outer vertical edges for safety
result = (
    slot
    .edges("|Z")
    .chamfer(chamfer_size)
)
