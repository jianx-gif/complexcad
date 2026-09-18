import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
cutout_size = 30.0
hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 90.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 2.0
rib_spacing = 20.0
chamfer_size = 1.0

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

cutout = (
    base.faces(">Z")
    .workplane()
    .rect(cutout_size, cutout_size)
    .cutBlind(-plate_thickness)
)

hole_positions = [
    (0, plate_width/2 - hole_offset),
    (0, -plate_width/2 + hole_offset),
    (plate_length/2 - hole_offset, 0),
    (-plate_length/2 + hole_offset, 0),
]

with_holes = (
    cutout.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, plate_thickness)
)

rib_count = int((plate_length - 2*hole_offset) // rib_spacing) + 1
rib_positions = [(-plate_length/2 + hole_offset + i*rib_spacing, 0) for i in range(rib_count)]

with_ribs = (
    with_holes.faces("<Z")
    .workplane()
    .pushPoints(rib_positions)
    .rect(rib_width, plate_width - 2*hole_offset)
    .extrude(rib_height)
)

result = (
    with_ribs.edges("|Z")
    .chamfer(chamfer_size)
)
