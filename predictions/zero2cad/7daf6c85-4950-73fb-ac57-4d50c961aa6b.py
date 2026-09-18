import cadquery as cq

# Parameters
leg_length_x = 80.0
leg_length_y = 60.0
leg_width = 20.0
thickness = 10.0
fillet_radius = 1.5
hole_diameter = 5.0
hole_offset = 12.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 15.0
rib_depth = 2.0

# Base L‑shape profile
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_length_x, 0),
        (leg_length_x, leg_width),
        (leg_width, leg_width),
        (leg_width, leg_length_y),
        (0, leg_length_y),
        (0, 0),
    ])
    .close()
)

# Extrude to create solid
base = profile.extrude(thickness)

# Fillet inner corner (edges parallel to X at the inner corner)
base = base.edges("|X and <Y").fillet(fillet_radius)

# Mounting holes on each leg (through‑thickness)
hole_positions = [
    (hole_offset, leg_width / 2),
    (leg_length_x - hole_offset, leg_width / 2),
    (leg_width / 2, hole_offset),
    (leg_width / 2, leg_length_y - hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Recessed ribs on the top face for stiffness
rib_count_x = int((leg_length_x - 2 * hole_offset) // rib_spacing)
rib_count_y = int((leg_length_y - 2 * hole_offset) // rib_spacing)

# Ribs on the X‑leg
base = (
    base.faces(">Z")
    .workplane()
    .center(hole_offset + rib_spacing / 2, leg_width / 2)
    .rarray(rib_spacing, 0, rib_count_x, 1)
    .rect(rib_width, rib_height)
    .cutBlind(rib_depth)
)

# Ribs on the Y‑leg
base = (
    base.faces(">Z")
    .workplane()
    .center(leg_width / 2, hole_offset + rib_spacing / 2)
    .rarray(0, rib_spacing, 1, rib_count_y)
    .rect(rib_width, rib_height)
    .cutBlind(rib_depth)
)

result = base