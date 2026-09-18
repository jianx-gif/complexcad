import cadquery as cq
outer_width = 80.0
outer_height = 60.0
wall_thickness = 2.0
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - 2 * wall_thickness
rib_width = 10.0
rib_height = 8.0
rib_spacing = 20.0
rib_count = 6
rib_count = 4
rib_count = 12
rib_spacing = 20.0
outer = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (outer_width, 0),
        (outer_width, outer_height - rib_spacing),
        (outer_width - rib_spacing, outer_height - rib_spacing),
        (outer_width - rib_spacing, outer_height - rib_spacing),
        (outer_width - rib_spacing, outer_height - rib_spacing),
        (outer_width - rib_spacing, outer_height - rib_spacing),
        (outer_width, outer_height - rib_spacing),
        (outer_width, outer_height),
        (0, outer_height),
    ])
    .close()
)
rib = (
    cq.Workplane("XY")
    .center(outer_width/2, outer_height/2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib_count = rib_count * rib_spacing
for i in range(rib_count):
    angle = i * 360.0 / rib_count
    rib_i = rib.rotate((0, 0, 0), (0, 0, 1), angle)
    rib_i = rib_i if i % 2 == 0 else rib_i if i % 2 == 0 else i % 0)
    rib_i = rib_i if i % 2 == 0 else rib_i if i % 2 == 0 if j % 2 == 0 is None else rib_i if j % 2 == 0 else rib_i if j % 2 == 0 else rib_i if j % 2 == 0 else rib_i + rib_spacing
rib = (
    cq.Workplane("XY")
    .center(outer_width/2, outer_height/2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = rib.union(rib)
