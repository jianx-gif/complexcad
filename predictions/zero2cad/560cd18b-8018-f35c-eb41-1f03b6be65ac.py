import cadquery as cq

plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
cutout_diameter = 30.0
rib_width = 8.0
rib_height = 6.0
rib_offset = 12.0
boss_diameter = 20.0
boss_height = 12.0
chamfer_distance = 1.5
hole_diameter = 4.0
hole_offset = 22.0

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

base = base.edges("|Z").chamfer(chamfer_distance)

base = (
    base.faces(">Z")
    .workplane()
    .circle(cutout_diameter / 2)
    .cutBlind(-plate_thickness)
)

rib1 = (
    base.faces(">Z")
    .workplane()
    .center(0, rib_offset)
    .rect(rib_width, plate_length)
    .extrude(rib_height)
)

rib2 = (
    base.faces(">Z")
    .workplane()
    .center(0, -rib_offset)
    .rect(rib_width, plate_length)
    .extrude(rib_height)
)

boss = (
    base.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

combined = base.union(rib1).union(rib2).union(boss)

hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (0, -hole_offset),
]

result = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
