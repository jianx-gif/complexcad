import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_distance = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius + rib_width, wall_thickness)
    .lineTo(inner_radius + rib_width, wall_thickness + rib_height)
    .lineTo(inner_radius + rib_width, wall_thickness + rib_height)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .circle(rib_width)
    .extrude(rib_height)
    .translate((inner_radius + rib_width/2, 0, wall_thickness + rib_height/2))
)
rib = rib.translate((inner_radius + rib_width/2, 0, wall_thickness + rib_height/2))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_distance)
result = combined
