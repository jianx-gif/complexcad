import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 8.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_end = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(arm_length, 0)
    .lineTo(arm_length, arm_width)
    .lineTo(arm_length, arm_width + arm_thickness)
    .lineTo(0, arm_width + arm_thickness)
    .close()
    .extrude(arm_length)
)
rib = (
    base.faces(">Z").workplane()
    .center(0, arm_width + rib_spacing)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .center(0, arm_width + rib_spacing)
    .rect(rib_width, rib_height)
    .cutBlind(-arm_thickness)
)
result = (
    result.faces(">Z").workplane()
    .center(0, arm_width + arm_length / 2)
    .rect(rib_width, arm_width)
    .cutBlind(-rib_height)
)
result = (
    result.faces(">Z").workplane()
    .center(0, arm_width + arm_length / 2)
    .rect(arm_length, arm_width)
    .cutBlind(-arm_thickness)
)
