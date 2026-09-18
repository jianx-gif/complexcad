import cadquery as cq
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 5.0
rib_height = 4.0
rib_width = 10.0
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
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib_pattern = rib.translate((0, plate_depth/2 - rib_width/2, plate_thickness/2))
rib_pattern = rib.translate((0, plate_depth/2 - rib_width/2, plate_thickness/2))
rib_pattern = rib_pattern.union(rib_pattern)
rib_pattern = rib_pattern.faces(">Z").workplane().hole(hole_diameter)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-plate_thickness)
rib_pattern = rib_pattern.union(rib_pattern)
result = rib_pattern
