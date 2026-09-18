import cadquery as cq
import math
outer_diameter = 30.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2
chamfer_distance = 0.5
rib_width = 6.0
rib_height = 10.0
rib_thickness = 4.0
rib_spacing = 12.0
rib_count = 4
outer_radius = outer_diameter / 2
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .lineTo(inner_radius + rib_width, wall_thickness + rib_thickness)
    .lineTo(inner_radius + rib_width, wall_thickness + rib_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .lineTo(inner_radius, wall_thickness + rib_thickness)
    .close()
)
result = base.cut(inner)
result = result.edges("|Z").chamfer(chamfer_distance)
