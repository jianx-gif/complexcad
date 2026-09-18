import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 6.0
rib_height = 10.0
rib_width = 12.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 15.0
rib_offset = 10.0
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
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_height)
combined = combined.faces(">Z").workplane().rarray(rib_spacing, 0, rib_count, 1).rect(rib_width, rib_height).extrude(rib_height)
combined = combined.union(rib)
result = combined
