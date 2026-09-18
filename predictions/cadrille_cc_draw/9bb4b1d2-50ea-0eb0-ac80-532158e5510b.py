import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_edge = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width),
        (arm_length - rib_width, arm_width),
        (arm_length - rib_width, arm_width + rib_height),
        (arm_length - rib_width, arm_width + rib_height),
        (arm_length, arm_width + rib_height),
        (arm_length, 0),
        (0, 0)
    ])
    .close()
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(arm_length / 2, arm_width / 2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base.union(rib)
result = (
    result.faces(">Z")
    .workplane()
    .center(arm_length / 2, arm_width / 2)
    .rect(rib_width, arm_width)
    .cutBlind(-arm_thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(arm_length / 2, arm_width / 2)
    .hole(hole_diameter)
)
