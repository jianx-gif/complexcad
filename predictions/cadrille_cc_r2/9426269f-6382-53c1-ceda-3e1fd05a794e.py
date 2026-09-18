import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset_x = 15.0
hole_offset_y = 10.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing, forConstruction=True)
    .extrude(rib_height)
)
rib = rib.edges("|Z").chamfer(chamfer_distance)
rib1 = rib.translate((0, 0, plate_thickness))
rib2 = rib.translate((0, 0, plate_thickness))
rib3 = rib.translate((0, 0, plate_thickness))
rib4 = rib.translate((0, 0, plate_thickness))
rib5 = rib.translate((0, 0, plate_thickness))
rib6 = rib5.union(rib1).union(rib2)
hole_positions = [
    (-hole_offset_x, -hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, hole_offset_y),
]
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
