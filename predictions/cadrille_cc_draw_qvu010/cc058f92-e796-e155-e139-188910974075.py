import cadquery as cq
arm_length = 80.0
arm_width = 12.0
arm_thickness = 6.0
arm_height = 12.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_thickness),
        (arm_width, arm_thickness),
        (arm_width, arm_height),
        (0, arm_height),
        (0, 0)
    ])
    .close()
    .extrude(arm_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(arm_length/2, arm_height/2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = (
    rib.faces(">Z").workplane()
    .center(arm_length/2, arm_height/2)
    .rect(rib_width, arm_thickness)
    .extrude(rib_height)
)
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .center(arm_length/2, arm_height/2)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z").workplane()
    .center(arm_length/2, arm_height/2)
    .hole(hole_diameter)
)
