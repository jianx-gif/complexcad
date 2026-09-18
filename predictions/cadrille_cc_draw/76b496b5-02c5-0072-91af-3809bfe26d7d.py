import cadquery as cq
arm_length = 70.0
arm_width = 20.0
arm_thickness = 10.0
arm_height = 12.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_edge = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(arm_length, rib_width)
    .extrude(arm_thickness)
    .translate((0, 0, arm_height))
)
rib = rib.translate((0, 0, arm_height))
rib = rib.translate((0, 0, arm_height + rib_height))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset_from_edge, arm_width/2),
    (-hole_offset_from_edge, arm_width/2),
    (hole_offset_from_edge, -hole_offset_from_edge),
    (-hole_offset_from_edge, -hole_offset_from_edge),
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined.edges("|Z").chamfer(chamfer_size)
