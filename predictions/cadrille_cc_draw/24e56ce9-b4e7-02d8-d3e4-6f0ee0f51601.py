import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_count = 4
rib_spacing = 15.0
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
rib_count = int(360 / rib_count)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .lineTo(inner_radius, rib_height + rib_width)
    .close()
)
result = profile.revolve()
