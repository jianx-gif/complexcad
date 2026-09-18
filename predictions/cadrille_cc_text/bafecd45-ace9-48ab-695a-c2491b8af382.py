import cadquery as cq
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0
tab_length = 15.0
tab_height = 20.0
tab_width = 8.0
slot_width = 8.0
slot_length = 30.0
slot_offset = 10.0
blind_hole_diameter = 6.0
blind_hole_depth = 4.0
csk_angle = 82.0
rib_thickness = 4.0
rib_height = 5.0
rib_offset = 5.0
chamfer_distance = 1.0
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0
mount_hole_offset = 12.0
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (bracket_length, 0),
        (bracket_length, bracket_thickness),
        (bracket_length - tab_length, bracket_thickness),
        (bracket_length - tab_length, bracket_thickness + tab_height),
        (0, bracket_thickness + tab_height),
        (0, 0)
    ])
    .close()
    .extrude(bracket_thickness)
    .edges("|Z")
    .chamfer(chamfer_distance)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-bracket_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(blind_hole_diameter, blind_hole_depth)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_thickness, bracket_width)
    .extrude(rib_height)
)
