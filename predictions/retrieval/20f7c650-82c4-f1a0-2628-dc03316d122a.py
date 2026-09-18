import cadquery as cq

rail_length = 100.0
rail_width = 40.0
rail_thickness = 5.0
outer_fillet = 5.0
slot_length = 15.0
slot_width = 5.0
slot_spacing = 20.0
num_slot_rows = 3
row_offset = 12.0
chamfer = 0.5
hole_diameter = 5.0
hole_offset = 8.0
rib_width = 20.0
rib_thickness = 2.0
lightening_hole_diameter = 8.0
lightening_hole_offset_y = 30.0

base = (
    cq.Workplane("XY")
    .rect(rail_width, rail_length)
    .extrude(rail_thickness)
    .edges("|Z")
    .fillet(outer_fillet)
)

result = base

rib = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rail_length - 2 * row_offset)
    .extrude(rib_thickness)
)
result = result.union(rib)

for row in range(num_slot_rows):
    y = -rail_length / 2 + row_offset + row * slot_spacing
    for x in (-rail_width / 4, rail_width / 4):
        result = (
            result.faces(">Z")
            .workplane()
            .center(x, y)
            .rect(slot_length, slot_width)
            .cutBlind(-rail_thickness - 0.01)
        )

for sign in (1, -1):
    result = (
        result.faces(">Z")
        .workplane()
        .center(0, sign * (rail_length / 2 - hole_offset))
        .hole(hole_diameter)
    )

result = (
    result.faces(">Z")
    .workplane()
    .center(0, lightening_hole_offset_y - rail_length / 2)
    .hole(lightening_hole_diameter)
)

result = result.edges().chamfer(chamfer)
