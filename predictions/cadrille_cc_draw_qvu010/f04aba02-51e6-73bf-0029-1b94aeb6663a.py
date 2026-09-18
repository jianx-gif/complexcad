import cadquery as cq
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 4.0
rib_height = 8.0
rib_width = 12.0
rib_spacing = 12.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_count = 6
hole_offset = 10.0
chamfer_size = 0.5
rib_count = int((plate_width - 2 * rib_spacing) / rib_spacing)
rib_length = plate_width - 2 * rib_spacing
rib_length = plate_depth - 2 * rib_spacing
rib_count = int((plate_width - 2 * rib_spacing) // rib_spacing)
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
    .faces(">Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_spacing / 2, -hole_spacing / 2),
        (hole_spacing / 2, -hole_spacing / 2),
        (-hole_spacing / 2, hole_spacing / 2),
        (hole_spacing / 2, hole_spacing / 2),
    ])
    .hole(hole_diameter)
)
