import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 40.0
plate_thickness = 5.0
slot_width = 8.0
slot_length = 30.0
slot_spacing = 20.0
hole_diameter = 5.5
hole_spacing_x = 20.0
hole_spacing_y = 10.0
chamfer_distance = 3.0
rib_height = 2.0
rib_width = 6.0
rib_length = 50.0

# Base plate
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Double slots (cut through thickness)
slot_positions = [(-slot_spacing/2, 0), (slot_spacing/2, 0)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(slot_positions)
    .rect(slot_width, slot_length)
    .cutBlind(-plate_thickness)
)

# Clearance holes (M5 clearance)
hole_positions = [
    (-hole_spacing_x/2, -hole_spacing_y/2),
    (hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, hole_spacing_y/2),
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Reinforcing rib on back side (adds material)
result = (
    result
    .faces("<Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
)

# Chamfer on the +X side edges (30 degree approx)
result = (
    result
    .edges("|X and >Z")
    .chamfer(chamfer_distance)
)
