import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base)
    .lineTo(inner_radius, base)
    .lineTo(inner_radius, base)
    .close()
    .revolve()
)
result = base
