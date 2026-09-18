import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 40.0
base_thickness = 10.0
rib_height = 8.0
rib_width = 8.0
rib_offset = 5.0
hole_diameter = 6.0
hole_depth = 8.0
hole_count = 5
chamfer_size = 1.0

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
rib_outer_radius = outer_radius - rib_offset
rib_inner_radius = rib_outer_radius - rib_width
hole_center_radius = (rib_inner_radius + rib_outer_radius) / 2.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, base_thickness)
    .lineTo(rib_inner_radius, base_thickness)
    .lineTo(rib_inner_radius, base_thickness + rib_height)
    .lineTo(rib_outer_radius, base_thickness + rib_height)
    .lineTo(rib_outer_radius, base_thickness)
    .lineTo(outer_radius, 0)
    .close()
)

# Revolve to create solid
solid = profile.revolve()

# Add blind holes on top face
solid = (
    solid
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_center_radius, startAngle=0, count=hole_count, angle=360)
    .hole(hole_diameter, depth=hole_depth)
)

# Apply chamfer to outer vertical edges
result = solid.edges("|Z").chamfer(chamfer_size)
