import cadquery as cq

# Parameters
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
chamfer_size = 3.0
hole_diameter = 5.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_depth = 2.0

# Base L‑shape profile
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_width, 0),
        (leg_width, leg_length - leg_width),
        (leg_width * 2, leg_length - leg_width),
        (leg_width * 2, leg_length),
        (0, leg_length),
    ])
    .close()
)

# Extrude to create solid
result = profile.extrude(thickness)

# Chamfer outer edges
result = result.edges(">X or >Y or >Z").chamfer(chamfer_size)

# Mounting holes on each leg (through thickness)
# Hole on vertical leg
result = (
    result.faces("<Z")
    .workplane()
    .center(leg_width / 2, leg_length - hole_offset)
    .hole(hole_diameter)
)
# Hole on horizontal leg
result = (
    result.faces("<Z")
    .workplane()
    .center(leg_width * 2 - hole_offset, leg_width / 2)
    .hole(hole_diameter)
)

# Add ribs on the top face for stiffness
rib_count = int((leg_length - 2 * hole_offset) // rib_spacing)
for i in range(rib_count):
    y_pos = hole_offset + i * rib_spacing + rib_spacing / 2
    result = (
        result.faces(">Z")
        .workplane()
        .center(leg_width / 2, y_pos)
        .rect(rib_width, rib_height)
        .cutBlind(-rib_depth)
    )

# Add a reinforcing gusset at the inner corner
gusset = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_width, 0),
        (0, leg_width),
    ])
    .close()
    .extrude(thickness)
)
result = result.union(gusset)
