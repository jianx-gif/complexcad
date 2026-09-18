import cadquery as cq
plate_width = 100.0
plate_height = 80.0
plate_thickness = 5.0
rib_width = 4.0
rib_height = 30.0
rib_thickness = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
hole_offset_x = 20.0
hole_offset_y = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
