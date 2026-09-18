import cadquery as cq
plate_length = 100.0
plate_width = 100.0
plate_thickness = 10.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
rib_spacing = 15.0
rib_offset = 5.0
chamfer_size = 0.5
base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.union(rib)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').edges().chamfer(chamfer_size)
result = combined
