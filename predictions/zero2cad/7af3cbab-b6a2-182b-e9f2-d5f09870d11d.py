import cadquery as cq

block_length = 80.0
block_width = 40.0
block_height = 20.0
fillet_radius = 2.0
chamfer_distance = 1.0
pocket_diameter = 30.0
pocket_depth = 12.0
countersink_diameter = 6.0
countersink_angle = 82.0
rib_thickness = 4.0
rib_height = 6.0
rib_spacing = 15.0
rib_count = 2

base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .edges("|Z")
    .fillet(fillet_radius)
    .edges()
    .chamfer(chamfer_distance)
)

pocketed = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(pocket_diameter / 2)
    .cutBlind(pocket_depth)
)

countersunk = (
    pocketed
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(countersink_diameter, block_height, countersink_angle)
)

ribbed = (
    countersunk
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .rarray(rib_spacing, 0, rib_count, 1)
    .rect(rib_thickness, rib_height)
    .extrude(rib_height)
)

result = ribbed
