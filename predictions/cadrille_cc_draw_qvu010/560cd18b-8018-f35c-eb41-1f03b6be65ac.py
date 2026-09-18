import cadquery as cq
plate_width = 80.0
plate_depth = 50.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_spacing = 12.0
rib_offset = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width - 2 * rib_spacing, plate_depth - 2 * rib_spacing)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().rect(rib_width, plate_depth).extrude(rib_height)
combined = combined.faces(">Z").workplane().rect(rib_width, plate_depth).cutBlind(-rib_height)
result = combined
