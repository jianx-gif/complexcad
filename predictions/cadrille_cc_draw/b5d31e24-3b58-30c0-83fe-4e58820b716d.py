import cadquery as cq
arm_length = 70.0
arm_width = 15.0
arm_thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 8
rib_count = 8
rib_count = 6
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_width)
    .translate((0, 0, arm_thickness))
)
rib = rib.translate((0, 0, arm_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, arm_width).cutBlind(-arm_thickness)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, arm_width).cutBlind(-arm_thickness)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, arm_width).cutBlind(-arm_thickness)
result = combined
