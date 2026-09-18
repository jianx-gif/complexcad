import cadquery as cq
plate_length = 100.0
plate_width = 80.0
plate_thickness = 4.0
rib_width = 6.0
rib_height = 3.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_edge = 10.0
chamfer_size = 0.5
base = cq.Workplane('XY').box(plate_length, plate_width, plate_thickness)
rib = (
    cq.Workplane('XY')
    .box(rib_width, plate_width, plate_thickness)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges('|Z').chamfer(chamfer_size)
hole_positions = [
    (-hole_offset_from_edge, -hole_spacing),
    ( hole_offset_from_edge, -hole_spacing),
    ( hole_offset_from_edge, -hole_spacing),
    (-hole_offset_from_edge, -hole_spacing),
    ( hole_offset_from_edge, -hole_spacing),
    ( hole_offset_from_edge, hole_spacing),
    (-hole_offset_from_edge, hole_spacing),
    ( hole_offset_from_edge, hole_spacing)
]
combined = combined.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = combined
