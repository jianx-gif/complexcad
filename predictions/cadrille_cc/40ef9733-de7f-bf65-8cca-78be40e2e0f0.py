import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_height = 10.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
base = cq.Workplane('XY').box(outer_radius, outer_radius, outer_radius)
rib = (
    cq.Workplane('XY')
    .box(rib_width, rib_height, rib_width)
    .translate((outer_radius - rib_width/2, 0, 0))
)
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
rib = rib.translate((