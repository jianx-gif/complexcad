import cadquery as cq

# Parameters
plate_length = 100.0
plate_width = 80.0
plate_thickness = 5.0
slot_length = 20.0
slot_width = 5.0
slot_spacing_x = 15.0
slot_spacing_y = 20.0
slot_rows = 2
slot_cols = 3
mount_hole_dia = 8.0
mount_edge_margin = 10.0
lever_arm_length = 40.0
lever_arm_width = 15.0
lever_hole_dia = 6.0
chamfer_size = 0.7
rib_thickness = 2.0
rib_width = 5.0

# Base plate
base = cq.Workplane("XY").rect(plate_length, plate_width).extrude(plate_thickness)

# Compute slot positions (center points)
slot_start_x = -plate_length/2 + (plate_length - (slot_cols*slot_length + (slot_cols-1)*slot_spacing_x))/2 + slot_length/2
slot_start_y = -plate_width/2 + (plate_width - (slot_rows*slot_width + (slot_rows-1)*slot_spacing_y))/2 + slot_width/2
slot_points = []
for i in range(slot_cols):
    for j in range(slot_rows):
        x = slot_start_x + i*(slot_length + slot_spacing_x)
        y = slot_start_y + j*(slot_width + slot_spacing_y)
        slot_points.append((x, y))

# Cut slots through the plate
result = base
for pt in slot_points:
    result = result.faces('>Z').workplane().center(pt[0], pt[1]).rect(slot_length, slot_width).cutBlind(-plate_thickness)

# Mounting holes at four corners
mount_points = [
    (-plate_length/2 + mount_edge_margin, -plate_width/2 + mount_edge_margin),
    ( plate_length/2 - mount_edge_margin, -plate_width/2 + mount_edge_margin),
    ( plate_length/2 - mount_edge_margin,  plate_width/2 - mount_edge_margin),
    (-plate_length/2 + mount_edge_margin,  plate_width/2 - mount_edge_margin)
]
for pt in mount_points:
    result = result.faces('>Z').workplane().center(pt[0], pt[1]).hole(mount_hole_dia)

# Lever arm protrusion
lever = cq.Workplane("XY").center(0, plate_width/2 + lever_arm_width/2).rect(lever_arm_length, lever_arm_width).extrude(plate_thickness)
result = result.union(lever)
# Lever arm hole (centered along length)
result = result.faces('>Z').workplane().center(lever_arm_length/2, plate_width/2 + lever_arm_width/2).hole(lever_hole_dia)

# Chamfer external edges of plate and lever
result = result.edges().chamfer(chamfer_size)

# Central reinforcement rib on bottom face (adds thickness)
rib = cq.Workplane("XY").center(0,0).rect(plate_length-20, rib_width).extrude(rib_thickness)
result = result.union(rib)
