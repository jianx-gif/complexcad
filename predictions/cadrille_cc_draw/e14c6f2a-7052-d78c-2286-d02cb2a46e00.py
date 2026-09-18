import cadquery as cq
outer_diameter = 80.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 0.5
rib_width = 4.0
rib_height = 1.0
rib_thickness = 1.0
rib_spacing = 12.0
rib_count = 6
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius - wall_thickness)
    .lineTo(inner_radius, outer_radius - wall_thickness)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_thickness)
    .translate((inner_radius + rib_thickness / 2.0, 0, 0))
)
rib = rib.translate((inner_radius + rib_thickness / 2.0, 0, 0))
rib = rib.translate((inner_radius + rib_thickness / 2.0, 0, 0))
combined = solid.union(rib)
combined = combined.edges().chamfer(chamfer_size)
result = combined
