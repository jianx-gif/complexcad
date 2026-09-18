import cadquery as cq

block_width = 80.0
block_length = 60.0
block_thickness = 12.0
wall_thickness = 3.0
bore_diameter = 15.0
clearance_hole_diameter = 5.0
clearance_hole_spacing = 20.0
rib_width = 8.0
rib_height = 5.0
rib_spacing = 12.0
lip_thickness = 2.0
lip_height = 6.0
lip_extension = 5.0
chamfer_distance = 0.5

# Base block with chamfer on vertical edges
result = (
    cq.Workplane('XY')
    .box(block_width, block_length, block_thickness, centered=True)
    .edges('|Z')
    .chamfer(chamfer_distance)
)

# Central bore through entire thickness
result = (
    result
    .faces('>Z')
    .workplane()
    .hole(bore_diameter)
)

# Clearance holes pattern on top face
hole_y_positions = [-clearance_hole_spacing, 0, clearance_hole_spacing]
points_holes = [(0, y) for y in hole_y_positions]
result = (
    result
    .faces('>Z')
    .workplane()
    .pushPoints(points_holes)
    .hole(clearance_hole_diameter)
)

# Rib pattern on top face
x_start = -block_width/2 + wall_thickness + rib_width/2
x_end = block_width/2 - wall_thickness - rib_width/2
rib_x_positions = []
pos = x_start
while pos <= x_end:
    rib_x_positions.append(pos)
    pos += rib_spacing
rib_points = [(x, 0) for x in rib_x_positions]
result = (
    result
    .faces('>Z')
    .workplane()
    .pushPoints(rib_points)
    .rect(rib_width, block_length)
    .extrude(rib_height)
)

# Snap‑fit lip on +X side
result = (
    result
    .faces('>X')
    .workplane()
    .rect(lip_thickness, lip_height)
    .translate((lip_thickness/2, 0, 0))
    .extrude(lip_extension)
)
