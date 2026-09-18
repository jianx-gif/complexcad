import cadquery as cq
arm_length = 80.0
arm_width = 20.0
arm_thickness = 12.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, arm_width)
    .extrude(rib_height)
    .translate((0, 0, arm_thickness))
)
result = base.union(rib)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, arm_length/2 - wall_thickness/2)
    .rect(rib_width, arm_width)
    .extrude(rib_height)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, arm_length/2 - wall_thickness/2)
    .rect(rib_width, arm_width)
    .extrude(rib_height)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, arm_length/2 - wall_thickness/2)
    .rect(rib_width, arm_width)
    .extrude(rib_height)
)
result = result.union(rib)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, arm_length/2 - wall_thickness/2)
    .rect(rib_width, arm_width)
    .extrude(rib_height)
)
result = result.edges("|Z").chamfer(chamfer_size)
