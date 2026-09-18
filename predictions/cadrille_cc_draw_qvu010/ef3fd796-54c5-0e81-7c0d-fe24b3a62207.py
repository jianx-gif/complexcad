import cadquery as cq
arm_length = 70.0
arm_width = 30.0
arm_thickness = 2.0
arm_height = 12.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 15.0
hole_count = 5
hole_offset = 10.0
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
    .extrude(arm_thickness)
)
arm = (
    arm.faces(">Z")
    .workplane()
    .center(0, arm_width / 2)
    .rect(arm_length - 2 * wall_thickness, arm_width - 2 * wall_thickness)
    .extrude(arm_thickness)
)
arm = arm.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
result = (
    arm.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
