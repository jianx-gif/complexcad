import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 12.0
rib_thickness = 2.0
rib_count = 6
chamfer_distance = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, inner_radius)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_height, rib_width)
    .translate((inner_radius + rib_thickness / 2.0, inner_radius + rib_height / 2.0, rib_thickness / 2.0))
)
combined = base.union(rib)
combined = combined.edges(">Z").chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
result = combined
