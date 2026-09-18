import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 3
hole_diameter = 5.0
hole_offset = 10.0
slot_width = 4.0
slot_length = 30.0
slot_offset = 15.0
pocket_length = 40.0
pocket_width = 30.0
pocket_depth = 4.0
fillet_radius = 1.5

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

rib_profile = (
    cq.Workplane("XY")
    .rect(rib_width, plate_length)
    .extrude(rib_height)
)

ribs = (
    base.faces(">Z").workplane()
    .rarray(0, rib_spacing, 1, rib_count)
    .add(rib_profile)
)

hole_positions = [
    (-plate_length/2 + hole_offset, -plate_width/2 + hole_offset),
    ( plate_length/2 - hole_offset, -plate_width/2 + hole_offset),
    (-plate_length/2 + hole_offset,  plate_width/2 - hole_offset),
    ( plate_length/2 - hole_offset,  plate_width/2 - hole_offset)
]

with_holes = (
    ribs.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

slot = (
    with_holes.faces(">Y").workplane()
    .center(0, slot_offset)
    .rect(slot_width, slot_length)
    .cutBlind(-plate_thickness)
)

pocket = (
    slot.faces(">Z").workplane()
    .center(0, 0)
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

result = (
    pocket.faces(">Z").edges()
    .fillet(fillet_radius)
)
