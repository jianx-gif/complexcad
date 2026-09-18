import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 8.0
arm_height = 12.0
wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
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
        (arm_length - 2 * wall_thickness, arm_height),
        (arm_length, arm_height),
        (arm_length, 0),
        (0, 0)
    ])
    .close()
    .extrude(arm_thickness)
)
arm = (
    base.faces(">Z").workplane()
    .center(arm_length/2, 0)
    .rect(arm_width, arm_thickness)
    .cutBlind(-arm_thickness)
)
arm = (
    arm.faces(">Z").workplane()
    .center(arm_length/2, 0)
    .rect(arm_width, arm_thickness)
    .cutBlind(-arm_thickness)
)
hole_positions = [
    (arm_length/2, arm_width/2),
    (arm_length/2, arm_height/2),
    (-arm_length/2, arm_height/2),
    (-arm_length/2, -arm_width/2),
    (arm_length/2, -arm_width/2),
]
result = (
    arm.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
