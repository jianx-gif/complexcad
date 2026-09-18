import cadquery as cq
outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 15.0
chamfer_size = 0.5
rib_count = int(rib_spacing)
rib_count = int(rib_count)
base = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, outer_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
result = rib
