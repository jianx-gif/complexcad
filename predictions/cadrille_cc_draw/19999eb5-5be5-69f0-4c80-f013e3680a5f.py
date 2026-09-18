import cadquery as cq
base_length = 80.0
base_width = 50.0
base_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 12.0
rib_count = 6
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(base_length - 2 * rib_spacing, base_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-rib_height)
result = combined
