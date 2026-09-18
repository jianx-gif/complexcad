import cadquery as cq
import math
outer_diameter = 12.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
chamfer_distance = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius + wall_thickness, inner_radius)
    .lineTo(inner_radius + wall_thickness, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().polarArray(radius=inner_radius, startAngle=0, count=4, angle=360).hole(inner_radius * 2)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
