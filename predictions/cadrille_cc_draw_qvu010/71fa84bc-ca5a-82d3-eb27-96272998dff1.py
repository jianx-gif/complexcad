import cadquery as cq
plate_length = 100.0
plate_width = 80.0
plate_thickness = 8.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 6
hole_offset = 10.0
chamfer_size = 0.5
base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, plate_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
hole_positions = [
    (-hole_spacing/2, -hole_offset),
    (hole_spacing/2, -hole_offset),
    (-hole_spacing/2, hole_offset),
    (hole_spacing/2, hole_offset),
    (hole_spacing/2, hole_offset + hole_spacing),
    (hole_spacing/2, hole_offset + hole_spacing)
]
result = (
    combined
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
