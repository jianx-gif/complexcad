import cadquery as cq

block_length = 70
block_width = 40
block_thickness = 10
rib_length = 60
rib_width = 30
rib_height = 5
hole_diameter = 5.5
hole_spacing_x = 20
hole_spacing_y = 20
num_holes_x = 2
num_holes_y = 2
edge_offset = 10
edge_chamfer = 1

hole_positions = [
    (
        -block_length / 2 + edge_offset + i * hole_spacing_x,
        -block_width / 2 + edge_offset + j * hole_spacing_y,
    )
    for i in range(num_holes_x)
    for j in range(num_holes_y)
]

result = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
    .edges("|Z")
    .chamfer(edge_chamfer)
)
