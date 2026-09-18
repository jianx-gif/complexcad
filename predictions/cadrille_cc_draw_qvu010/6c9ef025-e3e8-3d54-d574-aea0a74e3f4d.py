import cadquery as cq
import math
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
outer_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(outer_radius - wall_thickness))
result = solid
