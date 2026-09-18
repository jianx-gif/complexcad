import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 4.0
rib_height = 3.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 15.0
hole_spacing_y = 12.0
chamfer_size = 0.5
base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
hole_positions = [
    (-hole_spacing_x/2, -hole_spacing_y/2),
    ( hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    ( hole_spacing_x/2, hole_spacing_y/2),
]
for x, y in hole_positions:
    combined = (
        combined
        .faces('>Z')
        .workplane()
        .pushPoints(hole_positions)
        .hole(hole_diameter)
    )
rib = (
    combined
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined
