import cadquery as cq
plate_width = 80.0
plate_height = 30.0
plate_thickness = 6.0
rib_height = 4.0
rib_width = 12.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_end = 10.0
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset_from_end, hole_offset_from_end),
    (-hole_offset_from_end, hole_offset_from_end),
    (hole_offset_from_end, -hole_offset_from_end),
    (-hole_offset_from_end, hole_offset_from_end)
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
