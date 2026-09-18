import cadquery as cq
arm_length = 30.0
arm_width = 12.0
base_thickness = 8.0
web_width = 20.0
web_extra_thickness = 4.0
slot_width = 6.0
slot_length = 12.0
slot_depth = base_thickness
chamfer_size = 0.6
base = (
    cq.Workplane("XY")
    .rect(arm_width, arm_length)
    .extrude(base_thickness)
)
web = (
    cq.Workplane("XY")
    .rect(web_width, web_extra_thickness)
    .extrude(base_thickness)
)
combined = base.union(web)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = (
    combined.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
