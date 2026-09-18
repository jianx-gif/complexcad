import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset_x = 15.0
hole_offset_y = 10.0
chamfer_distance = 1.0
rib_count = int((plate_length - 2 * rib_spacing) // rib_spacing)
rib_positions = [(-plate_length/2 + rib_spacing/2, 0), (plate_length/2 - rib_spacing/2, 0)]
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_distance)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
