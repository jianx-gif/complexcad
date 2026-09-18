import cadquery as cq

# Parameters
horizontal_leg_length = 70.0
vertical_leg_length = 80.0
leg_thickness = 8.0
leg_width = 20.0
fillet_radius = 3.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset_from_base = 20.0

# Build L-shaped profile
profile = (
    cq.Workplane('XY')
    .polyline([
        (0, 0),
        (horizontal_leg_length, 0),
        (horizontal_leg_length, leg_width),
        (leg_width, leg_width),
        (leg_width, vertical_leg_length),
        (0, vertical_leg_length),
        (0, 0)
    ])
    .close()
)

# Extrude to solid
bracket = profile.extrude(leg_thickness)

# Fillet interior concave edge (corner at (leg_width, leg_width))
bracket = (
    bracket
    .edges()
    .filter(lambda e: abs(e.Center().x - leg_width) < 0.1 and abs(e.Center().y - leg_width) < 0.1)
    .fillet(fillet_radius)
)

# Chamfer outer edges
bracket = bracket.edges('>Z or >X or >Y').chamfer(chamfer_distance)

# Add five through holes on the vertical leg front face (+Y)
for i in range(5):
    y_pos = hole_offset_from_base + i * hole_spacing - vertical_leg_length / 2
    bracket = (
        bracket
        .faces('>Y')
        .workplane(centerOption='CenterOfBoundBox')
        .center(leg_width / 2, y_pos)
        .hole(hole_diameter)
    )

result = bracket