import cadquery as cq
import math
outer_radius = 30.0
wall_thickness = 3.0
inner_radius = outer_radius - wall_thickness
outer_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
chamfer_distance = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, outer_radius)
    .lineTo(outer_radius, outer_radius)
    .lineTo(outer_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2, depth=outer_radius - wall_thickness * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2, depth=outer_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2, depth=outer_radius * 2)
solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, depth=outer_radius * 2)
solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, depth=outer_radius * 2)
solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, depth=outer_radius * 2)
solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, depth=outer_radius * 2)
solid = solid.edges().chamfer(chamfer_distance)
result = solid
