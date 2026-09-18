import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_height = 3.0
rib_width = 5.0
hole_diameter = 8.0
hole_spacing_x = 20.0
hole_spacing_y = 20.0
hole_rows = 2
hole_cols = 3
edge_chamfer = 0.8

base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)

rib = (
    cq.Workplane('XY')
    .rect(plate_length, plate_width)
    .extrude(rib_height)
    .faces('>Z')
    .workplane()
    .rect(plate_length - 2 * rib_width, plate_width - 2 * rib_width)
    .cutBlind(-rib_height)
    .translate((0, 0, plate_thickness))
)

combined = base.union(rib)

hole_positions = []
start_x = -plate_length / 2 + rib_width + hole_spacing_x / 2
start_y = -plate_width / 2 + rib_width + hole_spacing_y / 2
for i in range(hole_cols):
    for j in range(hole_rows):
        x = start_x + i * hole_spacing_x
        y = start_y + j * hole_spacing_y
        hole_positions.append((x, y))

result = (
    combined
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
    .edges('|Z')
    .chamfer(edge_chamfer)
)
