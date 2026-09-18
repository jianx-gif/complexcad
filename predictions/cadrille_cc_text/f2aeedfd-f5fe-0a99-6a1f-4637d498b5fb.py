import cadquery as cq
arm_length = 80.0
arm_width = 8.0
arm_thickness = 20.0
relief_center = 30.0
relief_width = 12.0
relief_depth = 4.0
hole_diameter = 5.0
hole_offset = 10.0
hole_count = 6
hole_spacing = (arm_length - 2 * hole_offset) / (hole_count - 1)
slot_width = 4.0
slot_length = 30.0
slot_offset = 45.0
fillet_radius = 2.0
result = (
    cq.Workplane("XY")
    .rect(arm_width, arm_thickness)
    .extrude(arm_length)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(relief_width, relief_depth)
    .cutBlind(-relief_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(hole_diameter, counterbore_dia, counterbore_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(hole_diameter, counterbore_dia, counterbore_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_offset)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(hole_diameter, counterbore_dia, counterbore_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(hole_diameter, counterbore_dia, counterbore_depth)
)
