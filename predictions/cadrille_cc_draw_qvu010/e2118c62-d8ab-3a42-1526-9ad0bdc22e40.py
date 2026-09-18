import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
wall_thickness = 6.0
rib_height = 10.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
result = rib
