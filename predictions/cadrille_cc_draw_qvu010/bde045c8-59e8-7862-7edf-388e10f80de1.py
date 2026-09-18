import cadquery as cq
plate_length = 100.0
plate_width = 100.0
plate_thickness = 10.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset_from_end = 15.0
chamfer_size = 0.5
rib_count = int(plate_length // rib_spacing) + 1
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
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
hole_positions = [
    (-hole_spacing/2, -hole_offset_from_end),
    (hole_spacing/2, -hole_offset_from_end),
    (-hole_spacing/2, hole_offset_from_end),
    (hole_spacing/2, hole_offset_from_end)
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (-plate_length/2, 0)])
    .hole(hole_diameter)
)
