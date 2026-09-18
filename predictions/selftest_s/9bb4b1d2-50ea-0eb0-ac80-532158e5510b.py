import cadquery as cq

horizontal_leg_len = 80.0
vertical_leg_len = 50.0
wall_thickness = 5.0
bracket_depth = 10.0
chamfer_size = 0.5
m6_hole_dia = 10.0
m6_hole_depth = bracket_depth
hole8_dia = 8.0
hole8_depth = bracket_depth
hole_offset = 8.0
rib_slot_width = 2.0
rib_slot_height = wall_thickness
rib_slot_depth = 1.0
rib_spacing = 15.0
side_pocket_width = 3.0
side_pocket_height = wall_thickness
side_pocket_depth = 4.0
side_pocket_spacing = 20.0

cross_section = [
    (0, 0),
    (horizontal_leg_len, 0),
    (horizontal_leg_len, wall_thickness),
    (horizontal_leg_len - wall_thickness, wall_thickness),
    (horizontal_leg_len - wall_thickness, vertical_leg_len),
    (0, vertical_leg_len),
    (0, 0)
]

result = cq.Workplane("XY").polyline(cross_section).close().extrude(bracket_depth)
result = result.edges().chamfer(chamfer_size)
result = (
    result.faces(">Z").workplane()
    .moveTo(hole_offset, hole_offset)
    .circle(m6_hole_dia / 2)
    .cutBlind(-m6_hole_depth)
)
result = (
    result.faces(">Z").workplane()
    .moveTo(horizontal_leg_len - hole_offset, wall_thickness / 2)
    .circle(hole8_dia / 2)
    .cutBlind(-hole8_depth)
)
num_ribs = int((vertical_leg_len - 2 * hole_offset) / rib_spacing) + 1
rib_positions = [
    (hole_offset + i * rib_spacing, wall_thickness / 2) for i in range(num_ribs)
]
for x, y in rib_positions:
    result = (
        result.faces(">Z").workplane()
        .moveTo(x, y)
        .rect(rib_slot_width, rib_slot_height)
        .cutBlind(-rib_slot_depth)
    )
num_side_pockets = int((horizontal_leg_len - 2 * hole_offset) / side_pocket_spacing) + 1
for i in range(num_side_pockets):
    x = hole_offset + i * side_pocket_spacing
    result = (
        result.faces(">X").workplane()
        .moveTo(x, wall_thickness / 2)
        .rect(side_pocket_width, side_pocket_height)
        .cutBlind(-side_pocket_depth)
    )
