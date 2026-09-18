import cadquery as cq
from cadquery import selectors

block_length = 90.0
block_width = 40.0
block_height = 20.0
draft_angle = 3.0
slot_length = 30.0
slot_width = 8.0
slot_offset = 5.0
pin_hole_diameter = 10.0
hole_fillet_radius = 1.0
rib_thickness = 4.0
rib_height = 5.0
rib_spacing = 20.0

half_len = block_length/2
half_wid = block_width/2
slot_bottom = -half_wid + slot_offset

profile = (
    cq.Workplane('XY')
    .polyline([
        (-half_len, -half_wid),
        (half_len - slot_length, -half_wid),
        (half_len - slot_length, slot_bottom),
        (half_len, slot_bottom),
        (half_len, slot_bottom + slot_width),
        (half_len - slot_length, slot_bottom + slot_width),
        (half_len - slot_length, half_wid),
        (-half_len, half_wid),
    ])
    .close()
    .extrude(block_height, taper=draft_angle)
)

num_ribs = int((block_length - 2*slot_offset) / rib_spacing)
rib_base = profile.faces('+Z').workplane()

ribs = cq.Workplane('XY')
for i in range(num_ribs):
    x_offset = -half_len + slot_offset + rib_spacing/2 + i * rib_spacing
    rib = (
        rib_base
        .center(x_offset, 0)
        .rect(rib_thickness, block_width - 2*slot_offset)
        .extrude(rib_height)
    )
    ribs = ribs.union(rib)

part = profile.union(ribs)

result = (
    part
    .faces('>Z')
    .workplane()
    .hole(pin_hole_diameter)
    .edges('|Z')
    .fillet(hole_fillet_radius)
)
