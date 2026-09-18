import cadquery as cq
plate_length = 60.0
plate_width = 30.0
plate_thickness = 12.0
rib_height = 8.0
rib_width = 10.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 12.0
rib_count = 4
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = rib.translate((rib_spacing, 0, 0))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_height)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-plate_thickness)
result = combined
