import cadquery as cq

arm_length = 80.0
arm_width = 8.0
arm_thickness = 20.0
relief_center = 30.0
relief_width = 12.0
relief_depth = 4.0
hole_diameter = 5.0
counterbore_dia = 8.0
counterbore_depth = 2.0
hole_offset = 10.0
slot_width = 4.0
slot_length = 30.0
slot_offset = 45.0
fillet_radius = 2.0

base = (
    cq.Workplane('XY')
    .rect(arm_length, arm_thickness)
    .extrude(arm_width)
)

relief = (
    base
    .faces('>Y')
    .workplane()
    .center(relief_center - arm_length/2, 0)
    .rect(relief_width, arm_width)
    .cutBlind(relief_depth)
)

slot = (
    relief
    .faces('>Y')
    .workplane()
    .center(slot_offset - arm_length/2, 0)
    .rect(slot_length, slot_width)
    .cutBlind(arm_thickness)
)

hole = (
    slot
    .faces('<Z')
    .workplane()
    .center(-arm_length/2 + hole_offset, 0)
    .cboreHole(hole_diameter, counterbore_dia, counterbore_depth)
)

result = (
    hole
    .edges('>X')
    .fillet(fillet_radius)
)
