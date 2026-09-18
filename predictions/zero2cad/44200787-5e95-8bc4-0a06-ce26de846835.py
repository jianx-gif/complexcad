import cadquery as cq

# Parameters
leg_length_long = 80.0
leg_length_short = 50.0
leg_width = 15.0
thickness = 6.0
step_height = 3.0
step_length = 40.0
hole_diameter = 5.0
hole_depth = 4.0
hole_spacing = 20.0
hole_offset_from_corner = 10.0
chamfer_size = 0.5
rib_thickness = 2.0
rib_width = 3.0
rib_length = 30.0

# Base L‑shape profile
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_length_long, 0),
        (leg_length_long, leg_width),
        (leg_width, leg_width),
        (leg_width, leg_length_short),
        (0, leg_length_short),
        (0, 0),
    ])
    .close()
    .extrude(thickness)
)

# Stepped shoulder on the long leg
step = (
    base.faces(">Z")
    .workplane()
    .center(leg_length_long - step_length / 2, leg_width / 2)
    .rect(step_length, leg_width)
    .extrude(step_height)
)

# Reinforcing rib on the short leg
rib = (
    base.faces("<Z")
    .workplane()
    .center(leg_width / 2, leg_length_short / 2)
    .rect(rib_width, rib_length)
    .extrude(-rib_thickness)
)

# Combine base, step, and rib
combined = base.union(step).union(rib)

# Blind holes on the long leg
hole_positions = [
    (hole_offset_from_corner + i * hole_spacing, leg_width / 2)
    for i in range(3)
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, depth=hole_depth)
)

# Chamfer outer edges for safety
result = combined.edges("|Z").chamfer(chamfer_size)
