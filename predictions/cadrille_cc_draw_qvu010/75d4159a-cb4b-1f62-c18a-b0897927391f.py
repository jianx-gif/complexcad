import cadquery as cq
plate_length = 80.0
plate_width = 20.0
plate_thickness = 5.0
rib_height = 12.0
rib_width = 12.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_spacing = 15.0
chamfer_size = 0.5
base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)
rib = (
    cq.Workplane('XY')
    .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.edges().chamfer(chamfer_size)
result = combined
