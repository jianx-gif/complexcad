import cadquery as cq
outer_width = 70.0
outer_height = 80.0
thickness = 12.0
flange_thickness = 8.0
chamfer = 0.8
mount_hole_dia = 4.5
mount_hole_spacing = 30.0
set_screw_hole_dia = 3.0
set_screw_head_dia = 6.0
set_screw_head_depth = 4.0
set_screw_angle = 90.0
set_screw_head_depth = 5.0
base = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(thickness)
)
flange = (
    cq.Workplane("XY")
    .rect(flange_thickness, flange_thickness)
    .extrude(thickness)
)
flange = (
    flange
    .translate((0, 0, flange_thickness))
)
flange = (
    flange
    .translate((0, 0, flange_thickness))
)
flange = (
    flange
    .translate((0, 0, flange_thickness))
)
flange = (
    flange
    .workplane(offset=flange)
    .center(0, 0)
    .rect(set_screw_head_dia, set_screw_head_dia)
    .cutBlind(set_screw_angle)
)
result = flange
