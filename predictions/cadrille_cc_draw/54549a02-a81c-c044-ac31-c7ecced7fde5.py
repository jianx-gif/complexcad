import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 12.0
rib_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, plate_length)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.union(rib)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, plate_length)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
combined = base.union(rib)
combined = combined.edges('|Z').chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(rib_count)
combined = combined.faces('>Z').workplane().hole(rib_diameter)
combined = combined.faces('>Z').workplane().center(0, 0).hole(rib_diameter)
result = combined
