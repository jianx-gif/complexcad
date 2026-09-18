import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 12.0
rib_spacing = 12.0
rib_count = 6
rib_spacing = 15.0
rib_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').box(plate_length, plate_width, plate_thickness)
rib = (
    cq.Workplane('XY')
    .box(rib_width, plate_width, rib_height)
    .translate((0, 0, plate_thickness))
)
rib = (
    cq.Workplane('XY')
    .box(rib_width, plate_width, rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges('|Z').chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(rib_height)
combined = combined.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-rib_height)
result = combined
