import cadquery as cq
horizontal_leg_len = 80.0
vertical_leg_len = 50.0
wall_thickness = 5.0
bracket_depth = 10.0
rib_slot_width = 2.0
rib_slot_depth = 1.0
rib_slot_margin = 5.0
rib_count = 6
rib_spacing = 15.0
rib_slot_offset = vertical_leg_len / 2.0
chamfer_size = 0.5
m6_hole_dia = 10.0
m6_hole_count = 4
hole_offset = 8.0
hole_depth = bracket_depth - 2.0
side_pocket_width = 3.0
side_pocket_depth = 4.0
side_pocket_spacing = 20.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (horizontal_leg_len, 0),
        (horizontal_leg_len, vertical_leg_len),
        (0, vertical_leg_len),
    ])
    .close()
    .extrude(bracket_depth)
)
rib = (
    base.faces(">Z")
    .workplane()
    .center(0, rib_slot_offset)
    .rect(rib_slot_width, rib_slot_depth)
    .cutBlind(-bracket_depth)
)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (0, -hole_offset),
]
result = (
    hole_positions
    .workplane()
    .pushPoints(hole_positions)
    .circle(m6_hole_dia / 2)
    .cutBlind(-bracket_depth)
)
