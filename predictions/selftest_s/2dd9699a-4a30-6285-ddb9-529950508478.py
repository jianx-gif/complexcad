import cadquery as cq
import math

plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
mount_hole_diameter = 5.0
mount_hole_offset_x = 30.0
mount_hole_offset_y = 20.0
rib_width = 6.0
rib_spacing = 12.0
rib_height = 3.0
octagon_side = 20.0
octagon_depth = 4.0
fillet_radius = 1.5
slot_width = 4.0
slot_length = 20.0
slot_offset_y = 25.0

result = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)

hole_positions = [
    (-mount_hole_offset_x, -mount_hole_offset_y),
    ( mount_hole_offset_x, -mount_hole_offset_y),
    (-mount_hole_offset_x,  mount_hole_offset_y),
    ( mount_hole_offset_x,  mount_hole_offset_y)
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(mount_hole_diameter)

result = result.faces('>Z').workplane().center(0, slot_offset_y).rect(slot_width, slot_length).cutBlind(-plate_thickness)

num_ribs = int((plate_width - rib_spacing) // (rib_width + rib_spacing))
for i in range(num_ribs):
    y_pos = -plate_width/2 + rib_spacing + i*(rib_width + rib_spacing) + rib_width/2
    result = result.faces('>Z').workplane().center(0, y_pos).rect(rib_width, plate_length).extrude(rib_height)

octagon_radius = octagon_side / (2 * math.sin(math.pi/8))
result = result.faces('>Z').workplane().polygon(8, octagon_radius*2).cutBlind(-octagon_depth)

result = result.faces('>Z').edges().fillet(fillet_radius)
