import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .center(inner_radius, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
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
result = rib.union(rib)
