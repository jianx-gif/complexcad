import cadquery as cq

# Parameters
outer_radius = 25.0
inner_radius = 20.0
length = 80.0
rib_height = 2.0
rib_width = 10.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 3
hole_depth = 5.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, length - rib_width)
    .lineTo(outer_radius + rib_height, length - rib_width)
    .lineTo(outer_radius + rib_height, length)
    .lineTo(inner_radius, length)
    .close()
)

# Revolve to create hollow cylindrical shell with rib
shell = profile.revolve()

# Add blind holes on outer surface
result = shell
for i in range(hole_count):
    z_pos = (i + 1) * hole_spacing
    hole = (
        cq.Workplane("XY")
        .center(outer_radius - hole_depth / 2, 0)
        .circle(hole_diameter / 2)
        .extrude(hole_depth)
        .translate((0, 0, z_pos))
    )
    result = result.cut(hole)

# Chamfer top rim edges
result = result.faces(">Z").edges().chamfer(chamfer_size)
