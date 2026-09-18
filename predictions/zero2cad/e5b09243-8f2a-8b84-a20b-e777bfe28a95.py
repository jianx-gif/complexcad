import cadquery as cq
import math

# Parameters
outer_radius = 40.0
inner_radius = 30.0
wall_thickness = outer_radius - inner_radius
height = 30.0
spline_control_points = [
    (outer_radius, 0),
    (outer_radius * 0.9, height * 0.2),
    (outer_radius * 0.7, height * 0.5),
    (outer_radius * 0.5, height * 0.8),
    (outer_radius * 0.3, height),
]
chamfer_distance = 0.5
hole_diameter = 5.0
hole_count = 6
hole_radius = outer_radius - wall_thickness / 2.0

# Build outer profile with spline edge
wp = cq.Workplane("XY")
profile = (
    wp
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .spline(spline_control_points)
    .lineTo(inner_radius, height)
    .close()
)
# Revolve to create solid
solid = profile.revolve()
# Shell to create hollow interior
hollow = solid.shell(-wall_thickness)
# Chamfer all edges for safety
hollow = hollow.edges().chamfer(chamfer_distance)
# Add mounting holes on top face
result = (
    hollow
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter)
)
