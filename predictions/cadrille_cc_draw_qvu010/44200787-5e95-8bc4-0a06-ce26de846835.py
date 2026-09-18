import cadquery as cq
arm_length = 100.0
arm_width = 20.0
arm_thickness = 8.0
arm_height = 12.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, arm_width)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, arm_width)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (arm_length/2 - hole_offset, 0),
    (arm_length/2 - hole_offset, 0),
    (arm_length/2 - hole_offset, -arm_width/2),
    (arm_length/2 - hole_offset, -arm_width/2),
    (arm_length/2 - hole_offset, 0)
]
combined = combined.cut(hole_positions)
hole_positions = [
    (arm_length/2 - hole_offset, 0),
    (arm_length/2 - hole_offset, 0)
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = (
    combined.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, arm_thickness)
    .cutBlind(-rib_height)
)
result = combined.edges("|Z").chamfer(chamfer_size)
