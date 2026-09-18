import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_height = 8.0
rib_width = 10.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 15.0
rib_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count).edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count).cutBlind(-rib_height)
result = combined
