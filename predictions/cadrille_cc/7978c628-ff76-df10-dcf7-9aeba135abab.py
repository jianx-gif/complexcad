import cadquery as cq
plate_length = 80.0
plate_width = 80.0
plate_thickness = 8.0
rib_height = 6.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 20.0
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
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
result = rib.union(rib)
result = result.faces(">Z").workplane().hole(hole_diameter)
result = result.edges("|Z").chamfer(chamfer_size)
