import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_spacing = 12.0
rib_offset = 15.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_length)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_spacing_x, hole_spacing_y),
    (-hole_spacing_x, hole_spacing_y),
    (hole_spacing_x, hole_spacing_y),
    (-hole_spacing_x, -hole_spacing_y),
    (hole_spacing_x, -hole_spacing_y),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
