import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 5.0
arm_height = 20.0
wall_thickness = 3.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 15.0
hole_spacing_y = 12.0
hole_rows = 2
hole_cols = 3
hole_spacing_y = 10.0
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
hole_positions = [
    (arm_length/2 - hole_spacing_x, arm_width/2 - hole_spacing_y),
    (arm_length/2 - hole_spacing_y, arm_width/2 - hole_spacing_y),
    (-arm_length/2 + hole_spacing_y, arm_width/2 - hole_spacing_y)
]
result = (
    arm.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
