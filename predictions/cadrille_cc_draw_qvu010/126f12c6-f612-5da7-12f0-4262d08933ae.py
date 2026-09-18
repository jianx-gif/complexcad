import cadquery as cq
base_length = 80.0
base_width = 50.0
base_thickness = 5.0
rib_height = 12.0
rib_width = 12.0
rib_spacing = 15.0
rib_count = int((base_length - rib_width) / rib_spacing) + 1
rib_offset = 10.0
chamfer_size = 0.5
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
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
