import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_height = 8.0
rib_width = 12.0
rib_spacing = 12.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset_x = 20.0
hole_offset_y = 15.0
chamfer_size = 0.5
rib_count = int((plate_length - 2 * rib_spacing) / rib_spacing)
rib_positions = [(-plate_length/2 + rib_spacing/2, 0), (plate_length/2 - rib_spacing/2, 0)]
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z").workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter)
    .faces(">Z").workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter)
)
