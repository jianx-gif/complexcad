import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 20.0
step_radius = 22.0
step_height = 10.0
total_height = 60.0
flange_thickness = 5.0
flange_radius = 28.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_depth = 12.0
hole_count = 6
hole_pattern_radius = 25.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, total_height - step_height - flange_thickness)
    .lineTo(step_radius, total_height - step_height - flange_thickness)
    .lineTo(step_radius, total_height - flange_thickness)
    .lineTo(inner_radius, total_height - flange_thickness)
    .lineTo(inner_radius, total_height)
    .lineTo(flange_radius, total_height)
    .lineTo(flange_radius, total_height + flange_thickness)
    .lineTo(0, total_height + flange_thickness)
    .close()
)

# Revolve to create solid
solid = profile.revolve()

# Add blind holes on top flange
solid = (
    solid
    .faces(">Z")
    .workplane()
    .polarArray(0, 0, hole_pattern_radius, hole_count)
    .hole(hole_diameter, depth=hole_depth)
)

# Chamfer outer edge of top flange
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)

result = solid