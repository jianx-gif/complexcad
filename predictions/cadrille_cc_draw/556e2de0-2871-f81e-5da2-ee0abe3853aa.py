import cadquery as cq
import math
outer_diameter = 100.0
wall_thickness = 3.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
rib_width = 5.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_distance = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius - wall_thickness)
    .lineTo(inner_radius, outer_radius - wall_thickness)
    .lineTo(inner_radius, outer_radius - wall_thickness)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.edges("|Z").chamfer(chamfer_distance)
result = solid
