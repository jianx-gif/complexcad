import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 4.0
rib_width = 6.0
rib_height = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_count = 4
rib_count = 4
rib_count = 12
rib_spacing = 12.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib_count = int((inner_radius + rib_spacing) // rib_spacing)
rib_count = int((inner_radius + rib_spacing) // rib_spacing)
rib_count = rib_count * rib_spacing
rib_count = rib_count * rib_spacing
rib_positions = [(-rib_count, 0), (rib_count, 0)]
for x, y in rib_count:
    rib = (
        cq.Workplane("XY")
        .center(x, y)
        .rect(rib_width, rib_height)
        .extrude(thickness)
    )
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0, 0, thickness))
    rib = rib.translate((0,