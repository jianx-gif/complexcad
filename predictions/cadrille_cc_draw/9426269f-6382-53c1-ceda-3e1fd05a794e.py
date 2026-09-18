import cadquery as cq
plate_length = 90.0
plate_width = 60.0
plate_thickness = 4.0
rib_height = 3.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_edge = 10.0
chamfer_size = 0.5
base = (
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
result = base.union(rib)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .cutBlind(-plate_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .cutBlind(-plate_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .cutBlind(-plate_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .cutBlind(-plate_thickness)
)
