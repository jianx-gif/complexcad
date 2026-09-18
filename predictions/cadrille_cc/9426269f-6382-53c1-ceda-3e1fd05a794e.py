import cadquery as cq
plate_length = 90.0
plate_width = 60.0
plate_thickness = 4.0
rib_width = 12.0
rib_height = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 20.0
chamfer_size = 0.5
base_plate = (
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
rib_pattern = rib_pattern.faces(">Z").workplane().hole(hole_diameter)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_width).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_width).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_width).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_width).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_width).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_width).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.union(rib_pattern)
result = rib_pattern
