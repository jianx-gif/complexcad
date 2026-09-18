import cadquery as cq
clamp_length = 80.0
clamp_width = 30.0
clamp_thickness = 6.0
jaw_thickness = 8.0
jaw_length = 20.0
tab_length = 20.0
tab_width = 10.0
tab_thickness = 4.0
central_hole_diameter = 12.0
central_hole_depth = 4.0
blind_hole_diameter = 5.0
blind_hole_depth = 5.0
blind_hole_spacing = 15.0
blind_hole_count = 6
blind_hole_spacing = 4.0
hex_socket_diameter = 10.0
hex_socket_depth = 4.0
hex_offset_x = clamp_length / 2 - 5.0
hex_offset_y = clamp_thickness / 2 - 5.0
hex_offset_y = clamp_thickness / 2 - 5.0
result = (
    cq.Workplane("XY")
    .rect(clamp_length, clamp_width)
    .extrude(clamp_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(tab_length, tab_width)
    .cutBlind(-clamp_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(central_hole_diameter / 2)
    .cutBlind(-clamp_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(central_hole_diameter, blind_hole_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(hex_socket_diameter, hex_socket_depth)
    .cutBlind(-clamp_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(central_hole_diameter / 2)
    .cutBlind(-clamp_thickness)
)
