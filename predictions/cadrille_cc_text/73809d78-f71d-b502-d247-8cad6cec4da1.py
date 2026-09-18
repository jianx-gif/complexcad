import cadquery as cq
block_length = 90
block_width = 40
block_height = 20
draft_angle = 3
slot_length = 30
slot_width = 8
slot_offset = 5
rib_thickness = 4
rib_height = 5
rib_spacing = 20
rib_count = 4
pin_hole_diameter = 10
hole_fillet_radius = 1
base = cq.Workplane('XY').rect(block_length, block_width).extrude(block_height)
base = base.edges('|Z').fillet(pin_hole_diameter)
base = base.faces('>Z').workplane().center(0, 0).hole(hole_fillet_radius)
base = base.faces('>Z').workplane().center(0, 0).hole(pin_hole_diameter)
rib = rib_spacing
for i in range(rib_count):
    rib = rib.translate((0, rib_spacing, block_height/2 - rib_height/2))
    rib = rib.translate((0, rib_spacing, block_height/2 - rib_height/2))
    base = base.union(rib)
result = base
