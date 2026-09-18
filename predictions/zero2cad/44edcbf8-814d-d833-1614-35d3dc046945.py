import cadquery as cq

# Parameters
outer_radius = 30.0
wall_thickness = 4.0
inner_radius = outer_radius - wall_thickness
length = 80.0
rib_height = 4.0
rib_width = 15.0
rib_start = (length - rib_width) / 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 3
hole_offset = 10.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_start)
    .lineTo(outer_radius + rib_height, rib_start)
    .lineTo(outer_radius + rib_height, rib_start + rib_width)
    .lineTo(outer_radius, rib_start + rib_width)
    .lineTo(outer_radius, length)
    .lineTo(inner_radius, length)
    .close()
)

# Revolve to create hollow tube with rib
tube = profile.revolve()

# Chamfer top outer edge
tube = tube.faces(">Z").edges().chamfer(chamfer_size)

# Add mounting holes on top face, evenly spaced along length
hole_positions = [(hole_offset + i * hole_spacing, 0) for i in range(hole_count)]
result = (
    tube
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
