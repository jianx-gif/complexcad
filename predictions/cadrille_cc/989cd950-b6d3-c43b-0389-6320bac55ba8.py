import cadquery as cq
import math
outer_diameter = 30.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2
outer_radius = outer_diameter / 2
inner_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, 0)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(inner_radius)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().rect(outer_radius, outer_radius).cutBlind(-outer_radius * 2)
solid = solid.faces(">Z").edges().fillet(inner_radius)
result = solid
