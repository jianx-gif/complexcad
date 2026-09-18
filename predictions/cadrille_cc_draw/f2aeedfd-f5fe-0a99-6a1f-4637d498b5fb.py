import cadquery as cq
base_length = 80.0
base_width = 20.0
base_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
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
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width - 2 * rib_spacing)
    .extrude(base_thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_height)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-base_thickness)
result = combined
