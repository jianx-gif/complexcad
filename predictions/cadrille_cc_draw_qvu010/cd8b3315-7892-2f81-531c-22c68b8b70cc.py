import cadquery as cq
plate_length = 80.0
plate_width = 50.0
plate_thickness = 4.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
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
    .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
hole_positions = [
    (-plate_length/2 + hole_offset_x, -plate_width/2 + hole_offset_y),
    ( plate_length/2 - hole_offset_x, -plate_width/2 + hole_offset_y),
    (-plate_length/2 + hole_offset_x,  plate_width/2 - hole_offset_y),
    ( plate_length/2 - hole_offset_x,  plate_width/2 - hole_offset_y)
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
    .rect(plate_length - 2 * rib_spacing, rib_width)
    .extrude(rib_height)
)
result = combined
