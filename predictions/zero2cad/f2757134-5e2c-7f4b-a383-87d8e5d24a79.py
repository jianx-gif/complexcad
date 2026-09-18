import cadquery as cq

cover_length = 80.0
cover_width = 60.0
cover_thickness = 8.0
wall_thickness = 2.0
slot_width = 12.0
slot_length = 30.0
slot_offset = 10.0
chamfer_distance = 1.5
rib_height = 2.0
rib_width = 4.0
rib_spacing = 10.0
rib_count = int((cover_length - 2 * wall_thickness) // rib_spacing)

base = (
    cq.Workplane("XY")
    .rect(cover_length, cover_width)
    .extrude(cover_thickness)
)

hollow = (
    base
    .faces(">Z")
    .shell(-wall_thickness)
)

slot_cut = (
    hollow
    .faces(">Y")
    .workplane()
    .center(-cover_length/2 + slot_offset + slot_length/2, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-cover_thickness)
)

chamfered = (
    slot_cut
    .edges("|X and >Y and >Z")
    .chamfer(chamfer_distance)
)

ribbed = (
    chamfered
    .faces("<Z")
    .workplane()
    .rarray(rib_spacing, 0, rib_count, 1)
    .rect(rib_width, cover_width - 2 * wall_thickness)
    .cutBlind(-rib_height)
)

result = ribbed
