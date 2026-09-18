import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 0.5
rib_count = int((plate_length - 2 * rib_spacing) / rib_spacing)
rib_length = plate_length - 2 * rib_spacing
rib_width = plate_width - 2 * rib_spacing
rib_height = plate_thickness
rib_spacing = 15.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    rib.faces(">Z").workplane()
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
