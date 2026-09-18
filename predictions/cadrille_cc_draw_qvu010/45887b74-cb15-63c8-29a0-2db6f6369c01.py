import cadquery as cq
arm_length = 80.0
arm_width = 20.0
arm_thickness = 12.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_offset = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(arm_length, rib_width)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, arm_thickness))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(arm_length - 2 * wall_thickness, rib_width)
    .extrude(rib_height)
)
combined = combined.union(rib)
hole_positions = [
    (arm_length/2 - hole_offset, 0),
    (arm_length/2 - hole_offset, 0),
    (arm_length/2 - hole_offset, -arm_width/2),
    (-arm_length/2 + hole_offset, -arm_width/2 + hole_offset),
    (arm_length/2 - hole_offset, -arm_width/2 + hole_offset),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
