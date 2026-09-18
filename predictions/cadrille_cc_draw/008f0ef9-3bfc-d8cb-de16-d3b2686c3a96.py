import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_height = 8.0
rib_width = 12.0
rib_spacing = 15.0
rib_count = 6
hole_diameter = 8.0
hole_spacing = 20.0
hole_offset_x = 30.0
hole_offset_y = 20.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, plate_width, rib_height)
    .translate((0, 0, plate_thickness))
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, plate_width, rib_height)
    .translate((0, 0, plate_thickness))
)
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
result = combined
