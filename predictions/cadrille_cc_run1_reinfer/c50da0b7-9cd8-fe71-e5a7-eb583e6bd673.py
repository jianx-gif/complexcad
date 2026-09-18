import cadquery as cq
import math
outer_diameter = 30.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_diameter = inner_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius + wall_thickness
inner_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces(">Z").edges().chamfer(outer_radius)
solid = solid.faces("<Z").edges().chamfer(outer_radius)
solid = solid.faces("<Z").edges().chamfer(outer_radius)
solid = solid.faces("<Z").edges().chamfer(outer_radius)
result = solid
