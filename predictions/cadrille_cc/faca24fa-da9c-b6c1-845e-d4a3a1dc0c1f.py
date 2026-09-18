import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 5.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 20.0
chamfer_size = 0.5
base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib_pattern = rib.translate((0, 0, plate_thickness))
rib_pattern = rib_pattern.union(rib)
result = (
    base_plate
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = result.union(rib_pattern)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = result.edges("|Z").chamfer(chamfer_size)
