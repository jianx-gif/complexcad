import cadquery as cq

panel_width = 100.0
panel_height = 30.0
panel_thickness = 5.0
hole_diameter = 5.0
hole_spacing = 8.0
array_start_x = -((9) * hole_spacing) / 2.0
chamfer_dist = 0.75
pocket_width = 60.0
pocket_height = 12.0
pocket_depth = 2.0
rib_width = 10.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 20.0

# Base plate
result = cq.Workplane('XY').box(panel_width, panel_height, panel_thickness)
result = result.faces('>Z').workplane().center(0, 0).rect(pocket_width, pocket_height).cutBlind(-pocket_depth)

# Linear array of holes
hole_positions = [(array_start_x + i * hole_spacing, 0) for i in range(10)]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = result.edges('|Z').chamfer(chamfer_dist)

# Add ribs on back side
num_ribs = int((panel_width - rib_spacing) // rib_spacing) + 1
rib_x_positions = [-(panel_width/2) + rib_spacing/2 + i * rib_spacing for i in range(num_ribs)]
for x in rib_x_positions:
    rib = cq.Workplane('XY').workplane(offset=-panel_thickness/2).center(x, 0).rect(rib_width, rib_height).extrude(rib_thickness)
    result = result.union(rib)
