import cadquery as cq
outer_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
wall_thickness = 2.0
rib_height = 4.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 12.0
chamfer_size = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
inner = cq.Workplane('XY').circle(inner_radius).extrude(wall_thickness)
inner = inner.cut(inner)
rib = (
    cq.Workplane('XY')
    .center(inner_radius + rib_spacing, 0)
    .rect(rib_width, rib_height)
    .extrude(wall_thickness + rib_height)
)
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
rib = rib.translate((outer_radius + rib_width/2, 0, wall_thickness))
result = rib
