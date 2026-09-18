import cadquery as cq
base_length = 70.0
base_width = 30.0
base_thickness = 5.0
rib_width = 12.0
rib_height = 10.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 15.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
