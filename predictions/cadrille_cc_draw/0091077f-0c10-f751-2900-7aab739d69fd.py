import cadquery as cq
arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_spacing = 12.0
rib_offset = 5.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, arm_thickness))
)
rib = rib.translate((0, 0, arm_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_width)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, arm_width).cutBlind(-arm_thickness)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, arm_width).cutBlind(-arm_thickness)
result = combined
