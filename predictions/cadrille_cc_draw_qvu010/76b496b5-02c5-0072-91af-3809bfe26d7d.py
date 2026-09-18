import cadquery as cq
arm_length = 70.0
arm_width = 20.0
arm_thickness = 10.0
arm_height = 12.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_end = 15.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width),
        (arm_length - arm_width, arm_width),
        (arm_length - arm_width, arm_width - arm_height),
        (arm_length - arm_width, arm_width - arm_height),
        (arm_length, arm_width),
        (0, arm_width),
    ])
    .close()
    .extrude(arm_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(arm_length - rib_spacing, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = (
    rib.faces(">Z").workplane()
    .center(arm_length - rib_spacing, 0)
    .rect(rib_width, arm_width)
    .extrude(rib_height)
)
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
