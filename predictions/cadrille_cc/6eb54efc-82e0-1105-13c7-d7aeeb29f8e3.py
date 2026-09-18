import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 12.0
hole_spacing_y = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib_pattern = rib.translate((0, 0, plate_thickness))
rib_pattern = rib_pattern.union(rib)
rib_positions = [
    (-plate_length/2 + hole_spacing_x/2, -plate_width/2 + hole_spacing_y/2),
    ( plate_length/2 - hole_spacing_x/2, -plate_width/2 + hole_spacing_y/2),
    (-plate_length/2 + hole_spacing_x/2, -plate_width/2 + hole_spacing_y/2),
    ( plate_length/2 - hole_spacing_x/2, -plate_width/2 + hole_spacing_y/2),
    (-plate_length/2 + hole_spacing_x/2,  plate_width/2 - hole_spacing_y/2),
    (-plate_length/2 + hole_spacing_x/2,  plate_width/2 - hole_spacing_y/2),
    (-plate_length/2 + hole_spacing_x/2,  plate_width/2 - hole_spacing_y/2),
    (-plate_length/2 + hole_spacing_x/2,  plate_width/2 - hole_spacing_y/2),
    (-plate_length/2 + hole_spacing_x/2,  plate_width/2 - hole_spacing_y/2),
    (-plate_length/2 + hole_spacing_x/2,  plate_width/2 - hole_spacing_y/2),
    (-plate_length/2,  plate_width/2 - hole_spacing_y/2)
]
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_cols)
    .hole(hole_diameter)
)
