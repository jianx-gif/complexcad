import cadquery as cq

# Parameters
leg_length_x = 80.0
leg_length_y = 60.0
leg_width = 20.0
thickness = 2.0
inner_radius = 8.0
hole_diameter = 5.0
hole_offset = 15.0
chamfer_size = 0.5

# Base L‑profile with rounded inner corner
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_length_x, 0)
    .lineTo(leg_length_x, leg_width)
    .lineTo(leg_width + inner_radius, leg_width)
    .threePointArc((leg_width, leg_width), (leg_width, leg_width + inner_radius))
    .lineTo(leg_width, leg_length_y)
    .lineTo(0, leg_length_y)
    .close()
)

# Extrude to sheet thickness
solid = profile.extrude(thickness)

# Add mounting holes on each leg
hole_positions = [
    (hole_offset, leg_width / 2),
    (leg_length_x - hole_offset, leg_width / 2),
    (leg_width / 2, hole_offset),
    (leg_width / 2, leg_length_y - hole_offset),
]
for x, y in hole_positions:
    solid = solid.faces(">Z").workplane().center(x, y).hole(hole_diameter)

# Apply chamfer to outer edges for safety
result = solid.edges("|Z").chamfer(chamfer_size)
