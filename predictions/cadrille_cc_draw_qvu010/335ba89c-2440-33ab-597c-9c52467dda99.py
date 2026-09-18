import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 8.0
arm_height = 20.0
wall_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width),
        (arm_width, arm_width),
        (arm_width, arm_height),
        (0, arm_height),
    ])
    .close()
    .extrude(arm_thickness)
)
arm = (
    base.faces(">Z").workplane()
    .center(arm_length/2, 0)
    .rect(arm_width, arm_thickness)
    .extrude(arm_height)
)
arm = arm.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (arm_length/2 - hole_offset, 0),
    (arm_length/2 - hole_offset, 0)
]
hole_positions = [
    (arm_length/2 - hole_offset, 0)
]
result = (
    arm.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
