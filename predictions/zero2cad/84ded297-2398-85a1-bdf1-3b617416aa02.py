import cadquery as cq

bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 6.0
hole_offset_x = 20.0
hole_offset_y = 10.0
chamfer_distance = 1.0
slot_width = 6.0
slot_length = 20.0
slot_offset = 5.0

base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

slot = (
    base.faces(">Z")
    .workplane()
    .center(-bracket_length/2 + slot_offset, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-bracket_thickness/2)
)

hole_positions = [
    (-hole_offset_x, -hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, hole_offset_y),
]

holes = (
    slot.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

rib_count = int((bracket_length - 2 * rib_spacing) // rib_spacing) + 1
rib_positions = [(-bracket_length/2 + rib_spacing + i * rib_spacing, 0) for i in range(rib_count)]

ribs = (
    holes.faces("<Z")
    .workplane()
    .pushPoints(rib_positions)
    .rect(rib_width, bracket_width - 2 * rib_spacing)
    .extrude(-rib_height)
)

result = (
    ribs.edges("|Z")
    .chamfer(chamfer_distance)
)
