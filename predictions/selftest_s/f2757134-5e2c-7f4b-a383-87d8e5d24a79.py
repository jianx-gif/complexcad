import cadquery as cq

cover_length = 80
cover_width = 60
cover_thickness = 8
wall_thickness = 2
slot_width = 12
slot_leg_height = 25
slot_leg_length = 30
fillet_radius = 2
chamfer_dist = 1.5
mount_hole_dia = 5
mount_hole_spacing_x = 40
mount_hole_spacing_y = 30
rib_height = 4
rib_width = 10
rib_spacing = 15

# Base plate
base = cq.Workplane('XY').rect(cover_length, cover_width).extrude(cover_thickness)

# Hollow out to create wall thickness
hollow = base.faces('>Z').shell(-wall_thickness)

# Add recessed stiffening ribs on top surface (cut pockets)
num_ribs_x = int(cover_length // (rib_spacing * 2))
count_x = num_ribs_x * 2 + 1
hollow = (
    hollow.faces('>Z')
    .workplane()
    .rarray(rib_spacing * 2, 0, count_x, 1)
    .rect(rib_width, rib_spacing)
    .cutBlind(-rib_height)
)

# Create L-shaped slot on front (+Y) face via two rectangular cuts
# Vertical leg cut
hollow = hollow.faces('>Y').workplane().center(0, 0).rect(slot_width, slot_leg_height).cutBlind(-cover_thickness*1.5)
# Horizontal leg cut (offset to bottom of vertical leg)
hollow = hollow.faces('>Y').workplane().center(-slot_leg_length/2, -slot_leg_height/2).rect(slot_leg_length, slot_width).cutBlind(-cover_thickness*1.5)

# Add mounting holes on top surface (centered pattern)
hole = cq.Workplane('XY').circle(mount_hole_dia/2).extrude(cover_thickness*1.2)
positions = [
    (-mount_hole_spacing_x/2, -mount_hole_spacing_y/2),
    ( mount_hole_spacing_x/2, -mount_hole_spacing_y/2),
    (-mount_hole_spacing_x/2,  mount_hole_spacing_y/2),
    ( mount_hole_spacing_x/2,  mount_hole_spacing_y/2),
]
for dx, dy in positions:
    hollow = hollow.cut(
        hole.translate((dx, dy, cover_thickness/2 + 0.1))
    )

# Apply chamfer on handling edge (front top edge)
result = hollow.edges('(>Y and >Z)').chamfer(chamfer_dist)
