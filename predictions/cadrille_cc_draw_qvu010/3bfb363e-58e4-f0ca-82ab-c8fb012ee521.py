import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 15.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 4
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width),
        (arm_length - arm_width, arm_width),
        (arm_length - arm_width, arm_width + arm_width),
        (arm_length - arm_width, arm_width + arm_width),
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
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .center(arm_length - arm_width/2, 0)
    .rect(rib_width, arm_width)
    .extrude(arm_thickness)
)
result = result.edges("|Z").chamfer(chamfer_size)
