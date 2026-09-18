import cadquery as cq

cover_length = 80.0
cover_width = 60.0
cover_thickness = 5.0
wall_thickness = 2.0
pocket_length = 40.0
pocket_width = 20.0
pocket_depth = 2.0
latch_thickness = 1.5
latch_height = 10.0
latch_extension = 6.0
fillet_radius = 1.0
chamfer_distance = 0.5

base = (
    cq.Workplane("XY")
    .rect(cover_length, cover_width)
    .extrude(cover_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

pocket = (
    base.faces(">Z")
    .workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

latch = (
    pocket.faces(">X")
    .workplane()
    .rect(latch_thickness, latch_height)
    .extrude(latch_extension)
)

result = (
    latch
    .edges("|X")
    .chamfer(chamfer_distance)
)
