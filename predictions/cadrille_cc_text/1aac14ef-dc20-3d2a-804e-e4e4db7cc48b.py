import cadquery as cq
base_width = 60.0
base_depth = 30.0
base_thickness = 4.0
arm_length = 50.0
arm_start_width = 20.0
arm_end_width = 8.0
arm_angle = 45.0
fillet_radius = 0.8
pilot_hole_diameter = 3.0
pilot_hole_depth = 2.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_start_width, 0),
        (arm_start_width, base_depth),
        (arm_start_width + arm_end_width, base_depth),
        (arm_start_width + arm_end_width, base_depth + arm_angle),
        (0, base_depth + arm_angle),
        (0, 0)
    ])
    .close()
    .extrude(base_thickness)
)
arm = (
    base.faces(">Z")
    .workplane()
    .center(arm_start_width + arm_end_width, 0)
    .circle(pilot_hole_diameter / 2)
    .extrude(base_thickness)
)
arm = (
    arm.faces(">Z")
    .workplane()
    .center(arm_start_width + arm_end_width, 0)
    .rect(pilot_hole_depth, pilot_hole_diameter)
    .cutBlind(-pilot_hole_depth)
)
arm = (
    arm.faces(">Z")
    .workplane()
    .center(arm_start_width + arm_end_width, 0)
    .rect(pilot_hole_depth, pilot_hole_diameter)
    .cutBlind(-pilot_hole_depth)
)
arm = (
    arm.faces(">Z")
    .workplane()
    .center(arm_start_width + arm_end_width, 0)
    .circle(pilot_hole_diameter / 2)
    .extrude(base_thickness)
)
result = arm.union(arm)
