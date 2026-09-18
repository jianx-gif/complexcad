import cadquery as cq
import math
outer_diameter = 40.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2
chamfer_distance = 0.5
rib_width = 6.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 12.0
rib_count = 4
outer_radius = outer_diameter / 2
inner_radius = inner_radius + wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(wall_thickness)
)
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib = rib.translate((0, 0, -rib_height))
rib