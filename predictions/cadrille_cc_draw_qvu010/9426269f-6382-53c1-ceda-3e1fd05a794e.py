import cadquery as cq
plate_length = 90.0
plate_width = 60.0
plate_thickness = 4.0
rib_width = 12.0
rib_height = 6.0
rib_spacing = 15.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_end = 10.0
chamfer_size = 0.5
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
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (-hole_spacing/2, -hole_offset_from_end),
    (hole_spacing/2, -hole_offset_from_end),
    (-hole_spacing/2, hole_offset_from_end),
    (hole_spacing/2, hole_offset_from_end)
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
