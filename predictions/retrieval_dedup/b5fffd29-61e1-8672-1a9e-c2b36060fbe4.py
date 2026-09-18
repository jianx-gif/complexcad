import cadquery as cq

# Parameters
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 8.0
chamfer_distance = 4.0
recess_width = 30.0
recess_depth = 20.0
edge_margin = 10.0
hole_diameter = 5.5
slot_length = 50.0
slot_width = 8.0

hole_offset_x = plate_width / 2 - edge_margin
hole_offset_y = plate_depth / 2 - edge_margin
hole_positions = [
    (-hole_offset_x, -hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, hole_offset_y),
]

result = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .edges("|Z").chamfer(chamfer_distance)
    .faces(">Z").workplane()
    .rect(recess_width, recess_depth).cutThruAll()
    .faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
    .faces(">Z").workplane()
    .center(0, 0)
    .slot2D(slot_length, slot_width)
    .cutThruAll()
)
