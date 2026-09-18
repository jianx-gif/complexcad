import cadquery as cq

jaw_length = 80.0
jaw_width = 30.0
jaw_thickness = 10.0
corner_radius = 5.0
hole_diameter = 6.0
hole_depth = jaw_thickness - 2.0
slot_length = 30.0
slot_width = 6.0
slot_offset = corner_radius + 2.0
rib_width = 8.0
rib_height = 4.0
chamfer_size = 1.0
fillet_radius = 0.5

base = (
    cq.Workplane('XY')
    .rect(jaw_length, jaw_width)
    .extrude(jaw_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

with_hole = (
    base
    .faces('>Z')
    .workplane()
    .hole(hole_diameter, hole_depth)
)

slot_center_x = -jaw_length / 2 + slot_offset + slot_length / 2

left_slot = (
    with_hole
    .faces('>Z')
    .workplane()
    .center(slot_center_x, 0)
    .rect(slot_length, slot_width)
    .cutBlind(jaw_thickness)
)

right_slot = (
    left_slot
    .faces('>Z')
    .workplane()
    .center(-slot_center_x * 2, 0)  # mirror across center
    .rect(slot_length, slot_width)
    .cutBlind(jaw_thickness)
)

rib = (
    right_slot
    .workplane(offset=-jaw_thickness/2)
    .center(0, -jaw_width/2 + rib_width/2 + corner_radius)
    .rect(jaw_length - 2*corner_radius, rib_width)
    .extrude(rib_height)
)

chamfered = rib.edges('>Z').chamfer(chamfer_size)

final = chamfered.faces('>Z').edges().fillet(fillet_radius)

result = final