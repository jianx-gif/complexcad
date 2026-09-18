import cadquery as cq
plate_width = 30.0
plate_height = 20.0
plate_thickness = 6.0
rib_height = 4.0
rib_width = 10.0
rib_spacing = 12.0
rib_count = 12
rib_spacing = 12.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_width)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
result = combined
