import cadquery as cq

# Parameters
lever_length = 80.0
lever_width = 30.0
lever_thickness = 8.0
tslot_base_width = 12.0
tslot_width = 6.0
tslot_base_depth = 2.0
tslot_depth = 2.0
rib_thickness = 2.0
rib_height = 4.0
rib_end_margin = 5.0
rib_count = 3
cable_hole_diameter = 6.0
cable_hole_offset = -lever_length/2 + 15.0
chamfer_distance = 0.8

# Base plate
result = cq.Workplane("XY").box(lever_length, lever_width, lever_thickness)

# T-slot cut on top surface
pts = [
    (-tslot_base_width/2, 0),
    (-tslot_base_width/2, tslot_base_depth),
    (-tslot_width/2, tslot_base_depth),
    (-tslot_width/2, tslot_base_depth+tslot_depth),
    (tslot_width/2, tslot_base_depth+tslot_depth),
    (tslot_width/2, tslot_base_depth),
    (tslot_base_width/2, tslot_base_depth),
    (tslot_base_width/2, 0)
]
wp = result.faces(">Z").workplane()
wp = wp.polyline(pts).close()
result = wp.cutBlind(-(tslot_base_depth+tslot_depth))

# Ribbed reinforcement on bottom surface
rib_spacing = lever_width/(rib_count+1)
for i in range(rib_count):
    offset_y = -lever_width/2 + (i+1)*rib_spacing
    result = result.faces("<Z").workplane().center(0, offset_y).rect(rib_thickness, lever_length-2*rib_end_margin).extrude(rib_height)

# Cable tie hole on top surface
result = result.faces(">Z").workplane().center(cable_hole_offset, 0).hole(cable_hole_diameter)

# Chamfer outer vertical edges
result = result.edges("|Z").chamfer(chamfer_distance)
