import cadquery as cq
outer_radius = 40.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = inner_radius + wall_thickness
rib_height = 10.0
rib_width = 8.0
rib_spacing = 12.0
rib_count = 12
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(outer_radius, outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((outer_radius - rib_width / 2, 0, 0))
)
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0))
rib = rib.translate((outer_radius - rib_width / 2, 0, 0