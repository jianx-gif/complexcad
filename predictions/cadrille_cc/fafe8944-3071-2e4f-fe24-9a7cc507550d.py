import cadquery as cq
outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 4
rib_count = 4
rib_count = 12
rib_spacing = 12.0
chamfer_size = 0.5
outer = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(outer_height)
)
inner = (
    cq.Workplane("XY")
    .rect(outer_length - 2 * wall_thickness, outer_width - 2 * wall_thickness)
    .extrude(-wall_thickness)
)
rib_count = int((outer_width - 2 * wall_thickness) // rib_spacing)
rib_count = int((outer_width - 2 * wall_thickness) // rib_spacing)
rib_count = rib_count * rib_count
rib_positions = [
    (outer_length/2 - rib_spacing, outer_width/2 - rib_spacing),
    (outer_length/2 - rib_spacing, outer_width/2 - rib_spacing),
    (outer_length/2 - rib_spacing, outer_width/2 - rib_spacing),
    (outer_length/2 - rib_spacing, outer_width/2 - rib_spacing),
]
for x, y in rib_count:
    rib = (
        cq.Workplane("XY")
        .center(x, y)
        .rect(rib_width, rib_height)
        .extrude(rib_height)
    )
    rib = rib.translate((0, outer_width/2 - rib_spacing, 0))
    rib_i = rib.rotate((0, 0, 0), (0, 0, 1), 90)
    rib_i = rib.translate((0, outer_width/2 - rib_spacing, 0))
    rib_i = rib.translate((0, outer_width/2 - rib_spacing, 0))
rib_i = rib.translate((0, outer_width/2 - rib_spacing, 0))
rib2 = rib.translate((0, outer_width/2 - rib_spacing, 0))
rib3 = rib2.translate((0, outer_width/2 - rib_spacing, 0))
rib4 = rib2.translate((0, outer_width/2 - rib_spacing, 0))
result = rib_i.union(rib_i).union(rib2)
