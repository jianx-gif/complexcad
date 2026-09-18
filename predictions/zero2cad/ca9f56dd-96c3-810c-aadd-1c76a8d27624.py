import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 12.0
block_height = 40.0
base_thickness = 8.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_depth = 12.0
hole_count = 6
hole_radius = outer_radius - 3.0
rib_width = 4.0
rib_height = 20.0
rib_thickness = 3.0
rib_count = 4
rib_radius = inner_radius + 5.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, base_thickness)
    .lineTo(outer_radius, base_thickness)
    .threePointArc((outer_radius + 5, (base_thickness + block_height) / 2), (outer_radius, block_height))
    .lineTo(inner_radius, block_height)
    .close()
)

# Revolve to create axisymmetric block
result = profile.revolve()

# Chamfer top outer edge
result = result.faces(">Z").edges().chamfer(chamfer_size)

# Blind holes on top face
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter, depth=hole_depth)
)

# Add ribs on top face
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=rib_radius, startAngle=0, angle=360, count=rib_count)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
