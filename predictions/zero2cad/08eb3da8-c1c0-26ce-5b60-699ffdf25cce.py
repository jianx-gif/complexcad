import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 12.0
shoulder_radius = 18.0
shoulder_height = 15.0
total_height = 60.0
wall_thickness = outer_radius - inner_radius
chamfer_size = 0.8
hole_diameter = 4.0
hole_depth = 10.0
hole_count = 8
hole_radius = outer_radius - wall_thickness/2
tab_width = 20.0
tab_height = 10.0
tab_thickness = 5.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(shoulder_radius, 0)
    .lineTo(shoulder_radius, shoulder_height)
    .lineTo(outer_radius, shoulder_height)
    .lineTo(outer_radius, total_height)
    .lineTo(inner_radius, total_height)
    .lineTo(inner_radius, 0)
    .close()
)

# Revolve to create axisymmetric block
result = profile.revolve()

# Add a rectangular mounting tab on the bottom face
result = (
    result
    .faces("<Z")
    .workplane()
    .rect(tab_width, tab_height)
    .extrude(tab_thickness)
)

# Chamfer the top outer edge for safety
result = result.faces(">Z").edges().chamfer(chamfer_size)

# Create blind holes on the top face arranged in a polar array
result = (
    result
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter, depth=hole_depth)
)
