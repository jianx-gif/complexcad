import cadquery as cq

# Parameters
body_length = 60.0
body_radius = 20.0
flare_length = 30.0
flare_radius = 30.0
wall_thickness = 4.0
chamfer_size = 2.0
hole_diameter = 5.0
hole_depth = 8.0
hole_spacing = 15.0
hole_count = 3
hole_start_z = 10.0

# Outer profile sketch on XZ plane
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(body_radius, 0)
    .lineTo(body_radius, body_length)
    .lineTo(flare_radius, body_length + flare_length)
    .lineTo(0, body_length + flare_length)
    .close()
)

# Revolve to create solid body
solid_body = outer_profile.revolve()

# Shell to create hollow interior
hollow_body = solid_body.shell(-wall_thickness)

# Chamfer on flare exit edge (top face)
chamfered_body = hollow_body.faces(">Z").edges().chamfer(chamfer_size)

# Create blind holes pattern on outer cylindrical surface
hole_cylinders = cq.Workplane("XZ")
for i in range(hole_count):
    z_pos = hole_start_z + i * hole_spacing
    hole = (
        cq.Workplane("XZ")
        .center(body_radius - wall_thickness / 2, z_pos)
        .circle(hole_diameter / 2)
        .extrude(-hole_depth)
    )
    hole_cylinders = hole_cylinders.union(hole)

# Subtract holes from body
result = chamfered_body.cut(hole_cylinders)
