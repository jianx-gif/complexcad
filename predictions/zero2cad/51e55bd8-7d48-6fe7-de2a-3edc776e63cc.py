import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 30.0
step_diameter = 45.0
base_height = 20.0
step_height = 15.0
top_height = 6.0
fillet_radius = 0.5
chamfer_distance = 1.0
hole_diameter = 5.0
hole_depth = 12.0
hole_count = 6
hole_radius = (inner_diameter/2 + step_diameter/2) / 2

# Derived radii
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
step_radius = step_diameter / 2.0

# Create stepped profile and revolve
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(inner_radius, 0)
    .lineTo(inner_radius, base_height)
    .lineTo(step_radius, base_height)
    .lineTo(step_radius, base_height + step_height)
    .lineTo(outer_radius, base_height + step_height)
    .lineTo(outer_radius, base_height + step_height + top_height)
    .lineTo(0, base_height + step_height + top_height)
    .close()
)

solid = profile.revolve()

# Chamfer all edges for safety
solid = solid.edges().chamfer(chamfer_distance)

# Fillet all edges for smooth transition
solid = solid.edges().fillet(fillet_radius)

# Blind holes on top face arranged in a circle
result = (
    solid
    .faces(">Z")
    .first()
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter, depth=hole_depth)
)
