import cadquery as cq
import math
outer_diameter = 30.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = inner_radius + wall_thickness / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_radius, startAngle=0, count=hole_count, angle=360).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count).hole(hole_diameter)
solid = solid.edges(">Z").chamfer(chamfer_size)
result = solid
