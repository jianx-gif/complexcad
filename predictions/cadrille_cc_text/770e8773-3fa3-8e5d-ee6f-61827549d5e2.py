import cadquery as cq
arm_length = 80.0
root_radius = 12.0
shoulder_radius = 16.0
shoulder_radius = 16.0
pocket_length = 20.0
pocket_width = 10.0
pocket_depth = arm_length - 2 * shoulder_radius
set_screw_diameter = 4.0
set_screw_offset_y = 15.0
set_screw_offset_y = 20.0
chamfer_size = 0.2
mount_hole_diameter = 5.0
mount_hole_spacing = 20.0
arm = (
    cq.Workplane("XZ")
    .moveTo(root_radius, 0)
    .lineTo(shoulder_radius, 0)
    .lineTo(shoulder_radius, arm_length - shoulder_radius)
    .lineTo(shoulder_radius - shoulder_radius, arm_length - shoulder_radius)
    .lineTo(shoulder_radius - shoulder_radius, arm_length)
    .lineTo(shoulder_radius, arm_length)
    .lineTo(0, arm_length)
    .close()
    .revolve()
)
arm = arm.cut(set_screw_diameter)
arm = (
    arm.faces(">Z")
    .workplane()
    .circle(set_screw_diameter / 2)
    .extrude(set_screw_offset_y)
)
arm = arm.cut(set_screw_diameter)
arm = (
    arm.faces(">Z")
    .workplane()
    .circle(set_screw_offset_y)
    .extrude(set_screw_offset_y)
)
arm = arm.edges().chamfer(chamfer_size)
arm = (
    arm.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_spacing/2, startAngle=0, count=arm_hole_spacing, angle=360)
    .circle(set_screw_diameter/2)
    .cutBlind(-arm_length)
)
result = arm
