import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 20.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
outer = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius, thickness + wall_thickness)
    .lineTo(inner_radius + wall_thickness, thickness + wall_thickness)
    .lineTo(inner_radius + wall_thickness, thickness + wall_thickness)
    .lineTo(inner_radius, thickness + wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = outer.shell(-wall_thickness)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
