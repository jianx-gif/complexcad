import cadquery as cq
import math
outer_diameter = 30.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius + wall_thickness
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, base)
    .lineTo(inner_radius, base)
    .lineTo(outer_radius, base)
    .lineTo(outer_radius, base)
    .lineTo(outer_radius, 0)
    .close()
    .revolve()
)
result = base
