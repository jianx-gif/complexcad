import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 60.0
plate_thickness = 6.0
rib_width = 30.0
rib_height = 12.0
hole_diameter = 10.0
hole_circle_radius = 20.0
hole_count = 6
chamfer_dist = 1.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Top rib centered on plate
rib = (
    base
    .faces(">Z")
    .workplane()
    .rect(rib_width, plate_width)
    .extrude(rib_height)
)

# Bottom reinforcement rib (half height)
bottom_rib = (
    rib
    .faces("<Z")
    .workplane()
    .rect(rib_width, plate_width)
    .extrude(-rib_height/2)
)

# Through holes in circular pattern
holes = (
    bottom_rib
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(hole_diameter/2)
    .polarArray(hole_circle_radius, 0, 360, hole_count)
    .cutBlind(- (plate_thickness + rib_height))
)

# Chamfer outer vertical edges
result = (
    holes
    .edges("|Z")
    .chamfer(chamfer_dist)
)
