import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_width = 12.0
rib_height = 2.0
rib_length = plate_length - 20.0
hole_diameter = 8.0
hole_offset = 12.0
chamfer_size = 1.0
pocket_length = 30.0
pocket_width = 20.0
pocket_depth = 4.0
tab_length = 30.0
tab_thickness = 6.0
tab_height = 10.0

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

rib = (
    base.faces(">Z")
    .workplane()
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)

tab = (
    rib.faces(">Z")
    .workplane()
    .rect(tab_length, tab_thickness)
    .extrude(tab_height)
)

pocket = (
    tab.faces("<Z")
    .workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(pocket_depth)
)

hole_positions = [
    (-plate_length/2 + hole_offset, -plate_width/2 + hole_offset),
    ( plate_length/2 - hole_offset, -plate_width/2 + hole_offset),
    ( plate_length/2 - hole_offset,  plate_width/2 - hole_offset),
    (-plate_length/2 + hole_offset,  plate_width/2 - hole_offset)
]

with_holes = (
    pocket.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

result = (
    with_holes.edges("|Z")
    .chamfer(chamfer_size)
)
