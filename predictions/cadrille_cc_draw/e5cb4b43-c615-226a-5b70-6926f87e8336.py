import cadquery as cq
plate_length = 80.0
plate_width = 80.0
plate_thickness = 5.0
rib_height = 3.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
rib_count = 6
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 10.0
base = cq.Workplane('XY').box(plate_length, plate_width, plate_thickness)
rib = (
    cq.Workplane('XY')
    .box(rib_width, plate_length, rib_height)
    .translate((0, 0, plate_thickness))
)
rib = (
    cq.Workplane('XY')
    .box(rib_width, rib_height, rib_height)
    .translate((0, 0, plate_thickness))
)
combined = base.union(rib)
hole_positions = [
    (-plate_length/2 + hole_offset, -plate_width/2 + hole_offset),
    ( plate_length/2 - hole_offset, -plate_width/2 + hole_offset),
    (-plate_length/2 + hole_offset,  plate_width/2 - hole_offset),
    ( plate_length/2 - hole_offset,  plate_width/2 - hole_offset)
]
combined = (
    combined
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
