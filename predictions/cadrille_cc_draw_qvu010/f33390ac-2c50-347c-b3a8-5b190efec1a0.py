import cadquery as cq
arm_length = 80.0
arm_width = 15.0
arm_thickness = 5.0
arm_height = 10.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 4
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
arm = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
arm = arm.union(arm)
arm = (
    arm.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(arm_length - 2 * wall_thickness, arm_width - 2 * wall_thickness)
    .cutBlind(-arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
arm = arm.union(rib)
arm = (
    arm.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(arm_length - 2 * wall_thickness, arm_width - 2 * wall_thickness)
    .extrude(arm_thickness)
)
arm = arm.union(arm)
hole_positions = [
    (arm_length/2 - hole_offset, 0),
    (-arm_length/2 + hole_offset, 0),
    (arm_length/2 - hole_offset, -arm_width/2 + hole_offset),
    (-arm_length/2 + hole_offset, 0),
    (arm_length/2 - hole_offset, 0)
]
result = arm
