import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 12.0
rib_height = 5.0
rib_width = 12.0
rib_spacing = 12.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset_x = 20.0
hole_offset_y = 15.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_width, plate_width - 2 * rib_width)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
hole_positions = [
    (-hole_spacing / 2, -hole_offset_x),
    (hole_spacing / 2, -hole_offset_y),
    (-hole_spacing / 2, hole_offset_y),
    (hole_spacing / 2, hole_offset_y),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
