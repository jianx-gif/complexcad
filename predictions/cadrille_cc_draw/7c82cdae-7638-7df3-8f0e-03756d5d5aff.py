import cadquery as cq
arm_length = 80.0
arm_width = 20.0
arm_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_offset = 10.0
chamfer_size = 0.5
rib_count = int((arm_length - 2 * rib_spacing) / rib_spacing)
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width),
        (arm_length - 2 * arm_width, arm_width),
        (arm_length - 2 * arm_width, arm_width + rib_height),
        (arm_length - 2 * arm_width, arm_width + rib_height),
        (arm_length, arm_width + rib_height),
        (arm_length, 0),
    ])
    .close()
    .extrude(arm_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(0, arm_width/2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .center(0, arm_width/2)
    .rect(rib_width, arm_width)
    .cutBlind(-arm_thickness)
)
result = (
    result.faces(">Z").workplane()
    .center(0, arm_width/2)
    .rect(rib_width, arm_width)
    .cutBlind(-arm_thickness)
)
