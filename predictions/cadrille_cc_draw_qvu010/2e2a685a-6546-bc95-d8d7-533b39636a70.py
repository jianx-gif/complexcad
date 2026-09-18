import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 10.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset_x = 15.0
hole_offset_y = 10.0
base_plate = (
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
combined = base_plate.union(rib)
hole_positions = [
    (-hole_spacing / 2, hole_offset_x),
    (hole_spacing / 2, hole_offset_y),
    (-hole_spacing / 2, hole_offset_y),
    (hole_spacing / 2, hole_offset_y)
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
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined
