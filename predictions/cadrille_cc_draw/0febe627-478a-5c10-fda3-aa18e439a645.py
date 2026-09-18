import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 12.0
wall_thickness = 2.0
rib_width = 10.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 20.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .rect(plate_length - 2 * wall_thickness, plate_width - 2 * wall_thickness)
    .cutBlind(-plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
hole_positions = [
    (-plate_length/2 + hole_spacing_x/2, -plate_width/2 + hole_spacing_y/2),
    ( plate_length/2 - hole_spacing_x/2, -plate_width/2 + hole_spacing_y/2),
    (-plate_length/2 + hole_spacing_x/2,  plate_width/2),
    ( plate_length/2 - hole_spacing_x/2,  plate_width/2),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
