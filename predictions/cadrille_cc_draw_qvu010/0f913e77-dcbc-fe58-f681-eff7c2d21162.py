import cadquery as cq
plate_width = 50.0
plate_height = 80.0
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
    .rect(plate_width, plate_height)
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
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
result = (
    result.faces(">Z").workplane()
    .rect(plate_width - 2 * rib_spacing, rib_height - 2 * rib_spacing)
    .extrude(rib_height)
)
