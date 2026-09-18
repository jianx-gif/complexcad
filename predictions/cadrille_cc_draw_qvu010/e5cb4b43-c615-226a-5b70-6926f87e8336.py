import cadquery as cq
plate_width = 80.0
plate_height = 80.0
plate_thickness = 5.0
rib_height = 20.0
rib_width = 12.0
rib_thickness = 4.0
rib_spacing = 12.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
rib_count = int((plate_width - 2 * rib_spacing) / rib_spacing)
rib_positions = [(-plate_width/2 + rib_spacing/2 + i * rib_spacing) for i in range(rib_count)]
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(plate_width - 2 * rib_spacing, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(plate_width - 2 * rib_spacing, rib_thickness)
    .extrude(rib_height)
)
