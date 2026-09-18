import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 50.0
length = 60.0
taper_length = 15.0
wall_thickness = (outer_diameter - inner_diameter) / 2.0
chamfer_size = 2.0
keyway_width = 10.0
keyway_depth = 5.0
keyway_length = 30.0
keyway_offset = 10.0

# Derived radii
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# Base profile for revolve (outer shape with taper)
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, length - taper_length)
    .lineTo(inner_radius, length)
    .lineTo(0, length)
    .close()
)

# Revolve to create solid
solid = profile.revolve()

# Shell to create hollow interior
hollow = solid.shell(-wall_thickness)

# Chamfer outer edges for safety
chamfered = hollow.edges().chamfer(chamfer_size)

# Keyway cut: rectangular slot on outer surface
keyway = (
    cq.Workplane("XY")
    .center(0, length - keyway_offset - keyway_length / 2.0)
    .rect(keyway_width, keyway_depth)
    .extrude(keyway_length)
    .translate((0, 0, -keyway_length / 2.0))
)

# Subtract keyway from the part
result = chamfered.cut(keyway)
