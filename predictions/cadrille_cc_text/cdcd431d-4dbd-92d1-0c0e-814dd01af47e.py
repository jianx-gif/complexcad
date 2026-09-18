import cadquery as cq
bore_diameter = 20.0
bore_radius = bore_diameter / 2.0
collar_thickness = 12.0
set_screw_diameter = 44.0
set_screw_angle = 0.0
set_screw_head_diameter = 5.0
set_screw_head_diameter = set_screw_diameter + set_screw_head_diameter
set_screw_angle = 0.0
csk_depth = 2.0
csk_angle = 90.0
chamfer_distance = 0.7
vent_radius = 6.0
vent_height = collar_thickness * 0.6
vent_offset = 5.0
profile = (
    cq.Workplane("XZ")
    .moveTo(bore_radius, 0)
    .lineTo(bore_radius, collar_thickness)
    .lineTo(bore_radius + collar_thickness, collar_thickness)
    .lineTo(bore_radius + collar_thickness, collar_thickness + collar_thickness)
    .lineTo(bore_radius + collar_thickness, collar_thickness + collar_thickness)
    .lineTo(bore_radius, collar_thickness + collar_thickness)
    .lineTo(bore_radius, 0)
    .close()
)
result = profile.revolve()
result = result.edges().chamfer(chamfer_distance)
result = (
    result.faces(">Z")
    .workplane()
    .center(bore_radius + set_screw_head_diameter/2, 0)
    .rect(set_screw_head_diameter, set_screw_head_diameter)
    .cutBlind(-set_screw_angle)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(vent_radius)
    .cutBlind(-set_screw_depth)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(vent_radius)
    .cutBlind(-set_screw_depth)
)
result = result.edges().chamfer(chamfer_distance)
