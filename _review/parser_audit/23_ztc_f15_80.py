import cadquery as cq

base_length = 70.0
base_width = 45.0
base_thickness = 10.0
slot_length = 60.0
slot_width = 10.0
hole_diameter = 6.0
hole_offset_x = 20.0
hole_offset_y = 12.0
gusset_depth = 15.0
gusset_height = 25.0
overlap = 2.0
rib_width = 8.0
rib_height = 6.0
rib_spacing = 12.0

base = cq.Workplane('XY').box(base_length, base_width, base_thickness, centered=(True, True, False))
slot = cq.Workplane('XY').slot2D(slot_length, slot_width).extrude(base_thickness)
base = base.cut(slot)

hole_positions = [(-hole_offset_x, -hole_offset_y), (hole_offset_x, -hole_offset_y), (-hole_offset_x, hole_offset_y), (hole_offset_x, hole_offset_y)]
for x, y in hole_positions:
    base = base.faces('>Z').workplane().center(x, y).hole(hole_diameter)

gusset_profile = cq.Workplane('XY')\
    .moveTo(0, 0)\
    .lineTo(0, gusset_height)\
    .lineTo(gusset_depth, 0)\
    .close()\
    .extrude(base_thickness)

gusset_offset = base_length / 2 - overlap
gusset = gusset_profile.translate((gusset_offset, 0, 0))

result = base.union(gusset)

rib = cq.Workplane('XY').box(rib_width, base_width, rib_height, centered=(True, True, False))
rib = rib.translate((0, 0, -rib_height / 2))
num_ribs = int(base_length // rib_spacing)
rib_array = rib.translate((-(base_length / 2) + rib_spacing / 2, 0, 0))
for i in range(1, num_ribs):
    rib_array = rib_array.union(rib.translate(((i * rib_spacing), 0, 0)))
result = result.union(rib_array)
