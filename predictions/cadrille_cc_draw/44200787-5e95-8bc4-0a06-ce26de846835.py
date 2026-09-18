import cadquery as cq
arm_length = 70.0
arm_width = 20.0
arm_thickness = 8.0
arm_height = 12.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_size = 0.5
rib_count = int((arm_length - 2 * rib_spacing) / rib_spacing)
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, arm_width)
    .extrude(rib_height)
    .translate((0, 0, arm_height))
)
rib = rib.translate((0, 0, arm_height))
rib = rib.translate((0, 0, arm_height))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset, 0),
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, -hole_offset),
    (0, -hole_offset),
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined.edges("|Z").chamfer(chamfer_size)
