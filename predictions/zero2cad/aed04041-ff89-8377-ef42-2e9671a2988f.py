import cadquery as cq

# Parameters
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 5.0
hole_diameter = 5.0
hole_pitch_x = 25.0
hole_pitch_y = 25.0
holes_x = 3
holes_y = 2
slot_length = 70.0
slot_width = 4.0
chamfer_size = 0.5
rib_width = 12.0
rib_height = 2.0
rib_spacing = 30.0

# Base plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    # Add ribs on bottom face
    .faces("<Z").workplane()
    .rarray(rib_spacing, 0, 2, 1, True)
    .rect(rib_width, plate_depth - 10)
    .extrude(rib_height)
    # Drill holes on top face
    .faces(">Z").workplane()
    .rarray(hole_pitch_x, hole_pitch_y, holes_x, holes_y, True)
    .hole(hole_diameter)
    # Create longitudinal slot centered
    .faces(">Z").workplane()
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
    # Chamfer outer edges
    .edges("|Z").chamfer(chamfer_size)
)
