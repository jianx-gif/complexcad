import cadquery as cq
body_outer_dia = 60.0
body_inner_dia = 50.0
flange_thickness = 5.0
body_length = 40.0
thread_dia = 30.0
thread_length = 12.0
boss_dia = 22.0
boss_height = 15.0
chamfer = 1.0
mount_hole_dia = 5.0
mount_spacing = 30.0
mount_rows = 2
mount_cols = 3
mounting_spacing = mount_rows / 2
body = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(body_outer_dia / 2, 0)
    .lineTo(body_outer_dia / 2, body_length)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + flange_thickness)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + flange_thickness + 0.1)
    .lineTo(body_outer_dia / 2, body_length + fl0.1)
    .lineTo(body_outer_dia / 2, body_length + 0.1)
    .lineTo(body_outer_dia / 2, body_length + 0.