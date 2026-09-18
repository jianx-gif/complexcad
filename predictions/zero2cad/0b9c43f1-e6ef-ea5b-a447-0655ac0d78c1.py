import cadquery as cq

# Parameters
base_radius = 20.0
top_radius = 35.0
height = 80.0
wall_thickness = 2.0
chamfer_size = 0.8
hole_diameter = 4.0
hole_depth = 1.5
hole_count = 12
hole_pattern_radius = (base_radius + top_radius) / 2.0

# Create conical solid by revolving a profile
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(top_radius, height)
    .lineTo(0, height)
    .close()
)
solid_cone = profile.revolve()

# Shell to create thin-walled bellows
bellows = solid_cone.shell(-wall_thickness)

# Chamfer all edges for safety
bellows = bellows.edges().chamfer(chamfer_size)

# Add blind holes on the top face in a circular pattern
result = (
    bellows
    .faces(">Z")
    .first()
    .workplane()
    .polarArray(radius=hole_pattern_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter, depth=hole_depth)
)
