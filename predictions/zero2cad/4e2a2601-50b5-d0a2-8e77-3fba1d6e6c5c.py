import cadquery as cq

# Parameters
leg_length_long = 80.0
leg_length_short = 50.0
leg_width = 20.0
thickness = 8.0
hole_diameter = 6.0
countersink_diameter = 12.0
countersink_angle = 82.0
hole_spacing = 30.0
hole_offset_from_end = 15.0
chamfer_size = 1.0
pocket_width = 10.0
pocket_depth = 4.0

# Base L‑shape profile
profile = (
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
)

# Extrude to thickness
base = profile.extrude(thickness)

# Add a rectangular pocket on the inner corner for weight reduction
pocket = (
    base.faces(">Z")
    .workplane()
    .center(leg_width/2, leg_width/2)
    .rect(pocket_width, pocket_width)
    .cutBlind(-pocket_depth)
)

# Countersunk holes on the long leg
hole_positions = [
    (leg_length_long - hole_offset_from_end, leg_width/2),
    (leg_length_long - hole_offset_from_end - hole_spacing, leg_width/2),
]

with_holes = (
    pocket.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, thickness)
)

# Chamfer outer edges for safety
result = (
    with_holes.edges("|Z")
    .chamfer(chamfer_size)
)
