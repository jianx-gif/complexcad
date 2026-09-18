import cadquery as cq
arm_length = 70.0
arm_width = 20.0
arm_thickness = 10.0
arm_height = 15.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width),
        (arm_length, arm_height),
        (arm_length - 2 * wall_thickness, arm_height),
        (arm_length - 2 * wall_thickness, arm_height),
        (0, arm_height),
        (0, 0)
    ])
    .close()
    .extrude(arm_thickness)
)
arm = (
    base.faces(">Z").workplane()
    .center(arm_length - 2 * wall_thickness, arm_height / 2)
    .rarray(hole_spacing, 0, hole_spacing, 1)
    .hole(hole_diameter)
)
arm = (
    arm.faces(">Z").workplane()
    .center(arm_length - 2 * wall_thickness, arm_height / 2)
    .rarray(hole_spacing, 0, hole_spacing, 1)
    .hole(hole_diameter)
)
arm = (
    arm.faces(">Z").workplane()
    .center(arm_length - 2 * wall_thickness, arm_height / 2)
    .rarray(hole_spacing, 0, hole_spacing, 1)
    .hole(hole_diameter)
)
arm = (
    arm.faces(">Z").workplane()
    .center(arm_length - 2 * wall_thickness, arm_height / 2)
    .rarray(hole_spacing, 0, hole_spacing, 1)
    .hole(hole_diameter)
)
arm = arm.edges("|Z").chamfer(chamfer_size)
result = arm
