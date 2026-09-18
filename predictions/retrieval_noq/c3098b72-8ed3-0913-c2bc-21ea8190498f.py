import cadquery as cq

overall_diameter = 80.0
cap_height = 30.0
lip_height = 5.0
lip_thickness = 2.0
body_thickness = 4.0
set_screw_diameter = 4.0
set_screw_head_diameter = 8.0
set_screw_head_depth = 3.0
counterbore_diameter = 6.0
counterbore_depth = 5.0
chamfer_size = 0.8
mount_hole_diameter = 3.0
mount_hole_offset_angle = 30.0
mount_hole_count = 2
pocket_depth = 5.0
pocket_margin = 6.0

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(overall_diameter/2 - body_thickness, 0)
    .lineTo(overall_diameter/2 - body_thickness, cap_height - lip_height)
    .lineTo(overall_diameter/2, cap_height - lip_height)
    .lineTo(overall_diameter/2, cap_height)
    .lineTo(overall_diameter/2 - lip_thickness, cap_height)
    .lineTo(overall_diameter/2 - lip_thickness, cap_height - lip_height)
    .lineTo(overall_diameter/2 - body_thickness, cap_height - lip_height)
    .lineTo(overall_diameter/2 - body_thickness, 0)
    .close()
)

revolved = profile.revolve()

revolved = revolved.edges("( >> Z) and (<< X)").chamfer(chamfer_size)

revolved = (
    revolved
    .faces(">Z")
    .workplane()
    .hole(set_screw_diameter, depth=set_screw_head_depth)
    .faces(">Z")
    .workplane()
    .cskHole(set_screw_head_diameter, set_screw_head_depth, counterbore_diameter, counterbore_depth)
)

groove_depth = 1.0
revolved = (
    revolved
    .faces("<Z")
    .workplane(offset=cap_height - lip_height - groove_depth/2)
    .circle(overall_diameter/2 - body_thickness - groove_depth/2)
    .cutBlind(-groove_depth)
)

pocket_width = overall_diameter - 2*body_thickness - 2*pocket_margin
pocket_height = cap_height - lip_height - 2*pocket_margin
revolved = (
    revolved
    .faces(">Z")
    .workplane(offset=-pocket_depth/2)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)

angle_step = 360.0 / mount_hole_count
for i in range(mount_hole_count):
    revolved = (
        revolved
        .faces("<Z")
        .workplane(offset=cap_height/2)
        .polarArray(radius=overall_diameter/2 - body_thickness/2, startAngle=mount_hole_offset_angle + i*angle_step, count=1, angle=0)
        .hole(mount_hole_diameter)
    )

result = revolved