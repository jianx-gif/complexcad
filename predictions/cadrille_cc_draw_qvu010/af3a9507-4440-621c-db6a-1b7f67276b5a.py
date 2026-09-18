import cadquery as cq
arm_length = 80.0
arm_width = 20.0
arm_thickness = 8.0
arm_height = 20.0
wall_thickness = 3.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 8
hole_spacing = 12.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
arm = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(arm_length - 2 * wall_thickness, arm_width - 2 * wall_thickness)
    .cutBlind(-arm_thickness)
)
arm = (
    arm.faces(">Z")
    .workplane()
    .center(0, arm_width / 2)
    .rect(arm_length - 2 * wall_thickness, arm_width - 2 * wall_thickness)
    .extrude(arm_thickness)
)
rib = (
    arm.faces(">Z")
    .workplane()
    .center(0, arm_width / 2 - rib_spacing / 2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base.union(rib)
