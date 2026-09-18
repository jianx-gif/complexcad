import cadquery as cq
base_width = 60.0
base_thickness = 8.0
arm_length = 70.0
arm_start_width = 30.0
arm_end_width = 12.0
taper_angle = 10.0
fillet_radius = 2.0
chamfer_dist = 1.0
mount_hole_dia = 5.0
mount_hole_spacing = 40.0
groove_width = 20.0
groove_depth = 4.0
rib_thickness = 4.0
rib_width = 8.0
rib_height = 6.0
rib_count = 4
base = (
    cq.Workplane("XY")
    .rect(base_width, base_thickness)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)
arm = (
    cq.Workplane("XY")
    .rect(arm_start_width, arm_end_width)
    .extrude(arm_start_width)
    .translate((0, 0, arm_end_width))
)
arm = arm.union(arm)
arm = (
    arm.faces(">Z")
    .workplane()
    .center(0, arm_start_width/2 - arm_length/2)
    .rect(groove_width, arm_length)
    .extrude(groove_depth)
)
arm = arm.faces(">Z").edges().chamfer(chamfer_dist)
rib = (
    cq.Workplane("XY")
    .center(0, arm_start_width/2 - arm_length/2)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
arm = arm.union(rib)
result = arm
