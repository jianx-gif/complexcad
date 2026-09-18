import cadquery as cq

# Dimensions (max 100 units)
tank_outer_radius = 40.0
tank_height = 80.0
wall_thickness = 4.0
inner_radius = tank_outer_radius - wall_thickness

# Channel parameters
channel_radius = 2.0
channel_offset = inner_radius - channel_radius - 1.0
spiral_turns = 5
spiral_height = tank_height - 2 * wall_thickness
channel_chamfer = 0.5

# Chute parameters
chute_height = 20.0

# Chamfer for tank edges
outer_chamfer = 1.0

# Base tank (cylinder) without chamfer
outer_cyl = (
    cq.Workplane("XY")
    .circle(tank_outer_radius)
    .extrude(tank_height)
)

# Inner cavity
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(tank_height - wall_thickness)
)

tank_shell = outer_cyl.cut(inner_cyl)
# Apply chamfer to bottom rim of tank

tank_shell = tank_shell.edges("<Z").chamfer(outer_chamfer)

# Spiral channel via twistExtrude; start slightly above bottom to keep wall clearance
channel_profile = (
    cq.Workplane("XY")
    .center(channel_offset, 0)
    .circle(channel_radius)
)
spiral_channel = (
    channel_profile
    .twistExtrude(spiral_height, 360 * spiral_turns)
    .translate((0, 0, wall_thickness))
)

# Vertical chute extending downward from bottom interior
chute = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(channel_radius)
    .extrude(-chute_height)
)

# Combine channel and chute, add small chamfer to channel edges for safety
channel_assembly = (
    spiral_channel.union(chute)
    .edges(">>Z")
    .chamfer(channel_chamfer)
)

# Subtract channel assembly from tank shell
result = tank_shell.cut(channel_assembly)
