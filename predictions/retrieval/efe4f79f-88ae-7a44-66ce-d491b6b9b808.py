import cadquery as cq

rail_length = 100.0
rail_height = 20.0
rail_width = 30.0
shoulder_width = 10.0
shoulder_height = 12.0
shoulder_offset = 4.0
fillet_radius = 1.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 3
hole_start_offset = 15.0

# Base extrude of rail body
base = (
    cq.Workplane("XY")
    .rect(rail_width, rail_height)
    .extrude(rail_length)
)

# Recessed shoulder cut on one side (negative X face)
shoulder_cut = (
    base.faces("<X")
    .workplane()
    .center(-(rail_width/2 - shoulder_width/2), shoulder_offset + shoulder_height/2)
    .rect(shoulder_width, shoulder_height)
    .cutBlind(-rail_length/2)  # cut half depth for recessed
)

# Fillet on interior edges of shoulder cut
filleted = (
    shoulder_cut.edges("|Z and <X")
    .fillet(fillet_radius)
)

# Add chamfer on outer bottom edges for safety
chamfered = (
    filleted.edges("<Y and >Z")
    .chamfer(chamfer_distance)
)

# Through-hole pattern on top face
holes = (
    chamfered.faces(">Z")
    .workplane()
    .pushPoints([
        (hole_start_offset + i*hole_spacing - rail_width/2, 0) for i in range(hole_count)
    ])
    .hole(hole_diameter)
)

# Add fillet on top edges around holes
final = (
    holes.edges("<Z and >Y")
    .fillet(fillet_radius)
)

result = final