import cadquery as cq

# dimensions
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
wall_thickness = 2.0
frame_margin = 8.0
frame_height = 6.0
bottom_thickness = 2.0
chamfer_size = 0.5
fillet_size = 1.0
tap_diameter = 4.0
tap_depth = plate_thickness + frame_height - 2.0

# base plate creation
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness, centered=(True, True, False))
    .edges("|Z").fillet(fillet_size)
    .shell(-wall_thickness)
    # add bottom thickness to keep solid base
    .faces("<Z")
    .workplane()
    .rect(plate_length - 2*wall_thickness, plate_width - 2*wall_thickness)
    .extrude(bottom_thickness)
)

# raised frame on top
result = (
    base
    .faces(">Z")
    .workplane()
    .box(plate_length, plate_width, frame_height, centered=(True, True, False), combine=True)
    .faces(">Z")
    .workplane()
    .rect(plate_length - 2*frame_margin, plate_width - 2*frame_margin)
    .cutBlind(-frame_height)
    .edges("|Z").chamfer(chamfer_size)
)

# tap positions (seven holes)
# positions arranged symmetrically: four corners and three along center line
tap_positions = [
    (plate_length/2 - frame_margin, plate_width/2 - frame_margin),
    (-plate_length/2 + frame_margin, plate_width/2 - frame_margin),
    (plate_length/2 - frame_margin, -plate_width/2 + frame_margin),
    (-plate_length/2 + frame_margin, -plate_width/2 + frame_margin),
    (0, plate_width/2 - frame_margin),
    (0, -plate_width/2 + frame_margin),
    (0, 0),
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(tap_positions)
    .hole(tap_diameter)
)
