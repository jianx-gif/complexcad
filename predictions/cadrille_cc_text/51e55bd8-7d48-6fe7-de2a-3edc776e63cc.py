import cadquery as cq
bore_diameter = 23.0
collar_base_length = 15.0
shoulder_length = 10.0
shoulder_length = 12.0
shoulder_length = 10.0
set_screw_diameter = 4.0
set_screw_head_diameter = 7.0
set_screw_head_depth = 3.0
chamfer_size = 0.8
fillet_radius = 0.5
outer_diameter = 60.0
outer_radius = bore_diameter / 2.0
bore_radius = bore_radius - shoulder_length / 2.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(shoulder_length, 0)
    .lineTo(shoulder_length, collar_base_length)
    .lineTo(shoulder_length, collar_base_length + shoulder_length)
    .lineTo(0, collar_base_length + shoulder_length)
    .close()
)
bore = profile.revolve()
bore = bore.edges().fillet(fillet_radius)
bore = bore.edges().chamfer(chamfer_size)
bore = (
    bore
    .faces(">Z")
    .workplane()
    .circle(bore_radius)
    .extrude(bore_radius)
)
set_screw = (
    cq.Workplane("XY")
    .circle(set_screw_head_diameter / 2.0)
    .extrude(set_screw_head_depth)
)
result = (
    cq.Workplane("XY")
    .circle(set_screw_head_diameter / 2.0)
    .extrude(set_screw_head_depth)
    .translate((0, 0, collar_base_length + shoulder_length / 2.0))
)
