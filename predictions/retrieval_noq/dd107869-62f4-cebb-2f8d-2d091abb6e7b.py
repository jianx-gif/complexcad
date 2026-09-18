import cadquery as cq

cover_length = 80.0
cover_width = 60.0
cover_thickness = 8.0
rib_height = 6.0
rib_thickness = 3.0
rib_margin = 5.0
rib_length = cover_length - 2 * rib_margin
front_bevel_width = 1.0
mounting_hole_dia = 4.0
mounting_hole_spacing = 30.0
vent_slot_width = 20.0
vent_slot_height = 5.0
vent_slot_spacing = 12.0

base = (
    cq.Workplane("XY")
    .rect(cover_length, cover_width)
    .extrude(cover_thickness)
)

rib = (
    base.faces(">X").workplane()
    .rect(rib_thickness, rib_height)
    .extrude(rib_length)
)

with_rib = base.union(rib)

hole_y = cover_width / 2 - mounting_hole_spacing / 2
hole_positions = [(0, hole_y), (0, -hole_y)]

with_holes = (
    with_rib.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(mounting_hole_dia)
)

slot_offsets = [cover_width / 4, -cover_width / 4]
with_slots = with_holes
for offset in slot_offsets:
    with_slots = (
        with_slots.faces(">Y").workplane()
        .center(0, offset)
        .rect(vent_slot_width, vent_slot_height)
        .cutBlind(-cover_thickness)
    )

result = with_slots.faces(">Y").edges().chamfer(front_bevel_width)
