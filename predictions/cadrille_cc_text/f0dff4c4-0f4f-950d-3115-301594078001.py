import cadquery as cq
shaft_diameter = 30.0
collar_outer_diameter = 70.0
collar_outer_radius = shaft_diameter / 2.0
collar_outer_radius = collar_outer_diameter / 2.0
relief_groove_length = 3.0
relief_groove_depth = 8.0
set_screw_diameter = 5.0
set_screw_width = 8.0
set_screw_depth = 12.0
chamfer_size = 1.0
set_screw_depth = 12.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(shaft_diameter / 2.0, 0)
    .lineTo(shaft_diameter / 2.0, collar_width)
    .lineTo(collar_outer_radius, collar_width)
    .lineTo(collar_outer_radius, collar_width + collar_width)
    .lineTo(shaft_diameter / 2.0, collar_width + collar_width)
    .lineTo(shaft_diameter / 2.0, collar_width + collar_width + collar_width)
    .lineTo(shaft_diameter / 2.0, collar_width + collar_width + collar_width + collar_width)
    .lineTo(shaft_diameter / 2.0, collar_width + collar_width + collar_width + collar_width)
    .lineTo(shaft_diameter / 2.0, collar_width + collar_width + collar_width + collar_width)
    .lineTo(shaft_diameter / 2.0, collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width + collar_width +