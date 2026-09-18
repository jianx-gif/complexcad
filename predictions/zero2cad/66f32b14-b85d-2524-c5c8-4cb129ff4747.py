import cadquery as cq

# Parameters
plate_width = 80.0
plate_depth = 80.0
plate_thickness = 5.0
central_cutout_diameter = 30.0
hole_diameter = 6.0
hole_pitch = 20.0
hole_rows = 4
hole_cols = 4
slot_length = 60.0
slot_width = 6.0
slot_offset = 25.0
chamfer_size = 1.0

# Base plate with central cutout and chamfered vertical edges
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Central circular cutout through the plate
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(central_cutout_diameter / 2)
    .cutThruAll()
)

# Grid of sixteen through holes
base = (
    base
    .faces(">Z")
    .workplane()
    .rarray(hole_pitch, hole_pitch, hole_cols, hole_rows, True)
    .hole(hole_diameter)
)

# Two offset slots for adjustable fixtures
base = (
    base
    .faces(">Z")
    .workplane()
    .center(-slot_offset, 0)
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
    .center(2 * slot_offset, 0)
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
)

result = base
