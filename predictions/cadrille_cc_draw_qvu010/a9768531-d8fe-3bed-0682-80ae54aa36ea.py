import cadquery as cq
import math
outer_diameter = 30.0
inner_diameter = 20.0
wall_thickness = 2.0
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 4
hole_radius = inner_radius + wall_thickness / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius + wall_thickness, inner_radius)
    .lineTo(inner_radius + wall_thickness, inner_radius + wall_thickness)
    .lineTo(inner_radius + wall_thickness, inner_radius + wall_thickness)
    .lineTo(inner_radius, inner_radius + wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=hole_spacing / 2.0, startAngle=0, angle=360 / hole_count, angle=360 / hole_count)
    .hole(hole_diameter)
)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360 / hole_count, angle=360 / hole_count)
    .hole(hole_diameter)
)
result = solid
