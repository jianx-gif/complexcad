import cadquery as cq
plate_length = 80.0
plate_width = 50.0
plate_thickness = 5.0
boss_diameter = 30.0
boss_height = 10.0
groove_length = 40.0
groove_width = 6.0
groove_depth = 4.0
countersink_diameter = 10.0
hole_diameter = 6.0
countersink_angle = 82.0
hole_spacing_x = 30.0
hole_spacing_y = 20.0
chamfer_size = 0.5
base_plate = (cq.Workplane('XY')
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
# central boss
boss = (base_plate.faces('>Z')
    .workplane()
    .center(0, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)
combined = base_plate.union(boss)
# side groove on +X face
combined = (combined.faces('>X')
    .workplane()
    .rect(groove_length, groove_width)
    .cutBlind(-groove_depth)
)
# countersunk holes pattern (two rows of three)
hole_positions = [
    (-hole_spacing_x, -hole_spacing_y),
    (0, -hole_spacing_y),
    (hole_spacing_x, -hole_spacing_y),
    (-hole_spacing_x, hole_spacing_y),
    (0, hole_spacing_y),
    (hole_spacing_x, hole_spacing_y)
]
total_thickness = plate_thickness + boss_height
combined = (combined.faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(countersink_diameter, hole_diameter, countersink_angle, depth=total_thickness)
)
# chamfers on top edges and vertical edges of boss
result = (combined.edges('|Z')
    .chamfer(chamfer_size)
    .edges('>Z')
    .chamfer(chamfer_size)
)
