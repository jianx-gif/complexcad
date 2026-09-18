import cadquery as cq
plate_width = 80.0
plate_depth = 80.0
plate_thickness = 5.0
rib_height = 12.0
rib_width = 12.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 15.0
chamfer_size = 0.5
rib_count = 4
rib_spacing = 12.0
rib_spacing = 12.0
rib_count = 6
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = (
    rib.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
