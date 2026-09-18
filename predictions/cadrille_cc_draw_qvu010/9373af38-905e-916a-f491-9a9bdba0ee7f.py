import cadquery as cq
import math
outer_radius = 10.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_distance = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius + wall_thickness, outer_radius)
    .lineTo(inner_radius + wall_thickness, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.edges().chamfer(chamfer_distance)
result = solid
