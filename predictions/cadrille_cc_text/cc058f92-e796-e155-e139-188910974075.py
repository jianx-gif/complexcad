import cadquery as cq
horizontal_leg_length = 80.0
vertical_leg_length = 70.0
bracket_thickness = 6.0
extrude_length = 12.0
pocket_width = 20.0
pocket_depth = 4.0
chamfer_size = 0.5
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
counterbore_dia = 3.0
counterbore_offset_from_bottom = 20.0
set_screw_dia = 3.0
set_screw_offset = (horizontal_leg_length - 2 * mount_hole_spacing) / 2
mount_hole_spacing = (horizontal_leg_length - 2 * mount_hole_spacing) / 2
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (horizontal_leg_length, 0),
        (horizontal_leg_length, vertical_leg_length),
        (bracket_thickness, vertical_leg_length),
        (bracket_thickness, bracket_thickness),
        (0, bracket_thickness),
        (0, 0)
    ])
    .close()
    .extrude(extrude_length)
)
bracket = base.edges("|Z").chamfer(chamfer_size)
bracket = (
    bracket
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_dia)
)
bracket = (
    bracket
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_dia)
)
result = bracket
