import cadquery as cq
import math
outer_radius = 8.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
wall_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_spacing = wall_thickness + 2.0
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness + wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .close()
)
solid = profile.revolve(360)
hole_positions = [(-hole_spacing/2, 0), (hole_spacing/2, 0)]
solid = solid.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_diameter)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
