import cadquery as cq

# Core dimensions
arm_length = 80.0
root_radius = 12.0
shoulder_radius = 16.0
outer_radius = 20.0
pocket_length = 20.0
pocket_width = 10.0
set_screw_diameter = 4.0
set_screw_offset_y = 15.0
thread_length = 15.0
mount_hole_diameter = 5.0
mount_hole_spacing = 20.0
chamfer_size = 0.2

# 1) Base revolved profile (closed composite shape)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(root_radius, 0)
    .lineTo(root_radius, arm_length - pocket_length - thread_length)
    .lineTo(shoulder_radius, arm_length - pocket_length - thread_length)
    .lineTo(outer_radius, arm_length - pocket_length)
    .lineTo(root_radius, arm_length - pocket_length)
    .lineTo(root_radius, arm_length)
    .lineTo(0, arm_length)
    .close()
)
solid = profile.revolve()

# 2) Internal rectangular pocket for weight reduction
pocket_box = (
    cq.Workplane("XY")
    .center(outer_radius - pocket_width/2.0, arm_length/2.0)
    .box(pocket_width, pocket_length, outer_radius*2)
)
solid = solid.cut(pocket_box)

# 3) Blind threaded hole for adjustment set screw (clearance cylinder)
thread_cutter = (
    cq.Workplane("YZ")
    .center(set_screw_offset_y, 0)
    .workplane(offset=outer_radius)
    .circle(set_screw_diameter/2.0)
    .extrude(-thread_length)
)
solid = solid.cut(thread_cutter)

# 4) Pair of mounting holes at the base for assembly
hole1 = (
    cq.Workplane("XZ")
    .center(-mount_hole_spacing/2, 0)
    .circle(mount_hole_diameter/2)
    .extrude(arm_length)
)
hole2 = (
    cq.Workplane("XZ")
    .center(mount_hole_spacing/2, 0)
    .circle(mount_hole_diameter/2)
    .extrude(arm_length)
)
solid = solid.cut(hole1).cut(hole2)

# 5) Chamfer outer cylindrical edges for safety
solid = solid.edges("|Y").chamfer(chamfer_size)

result = solid