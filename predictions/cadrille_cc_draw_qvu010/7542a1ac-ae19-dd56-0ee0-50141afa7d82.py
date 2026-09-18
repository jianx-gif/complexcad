import cadquery as cq
import math
outer_radius = 15.0
wall_thickness = 3.0
inner_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, profile_thickness)
    .lineTo(inner_radius, profile_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
result = solid
