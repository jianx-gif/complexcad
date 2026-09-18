import cadquery as cq

plate_length = 100.0
plate_width = 30.0
plate_thickness = 5.0
rail_thickness = 3.0
rail_height = 10.0
hole_diameter = 5.0
hole_depth = 3.0
chamfer_size = 0.3
num_holes = 5
hole_spacing = 20.0
edge_margin = 10.0
mount_hole_dia = 4.0
mount_spacing = 40.0

base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

rail = (
    cq.Workplane("XY")
    .rect(plate_width, rail_thickness)
    .extrude(rail_height)
    .translate((0, 0, plate_thickness))
)

result = base_plate.union(rail)

hole_positions = [
    (-plate_length/2 + edge_margin + i * hole_spacing, 0)
    for i in range(num_holes)
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, depth=hole_depth)
)

result = result.edges("%CIRCLE").chamfer(chamfer_size)

mount_positions = [
    (-plate_length/2 + edge_margin/2, -plate_width/2 + edge_margin/2),
    (plate_length/2 - edge_margin/2, -plate_width/2 + edge_margin/2),
    (-plate_length/2 + edge_margin/2, plate_width/2 - edge_margin/2),
    (plate_length/2 - edge_margin/2, plate_width/2 - edge_margin/2)
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(mount_positions)
    .hole(mount_hole_dia)
)
