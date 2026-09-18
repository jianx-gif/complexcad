import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 8.0
arm_height = 12.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_count = 8
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .sketch()
    .rect(arm_width, arm_thickness)
    .rect(arm_width, arm_height)
    .finalize()
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, arm_thickness)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, arm_height - rib_height))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (arm_length/2 - hole_spacing, 0),
    (arm_length/2 - hole_spacing, 0),
    (arm_length/2 - hole_spacing, 0),
    (0, arm_width/2 - hole_spacing)
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
