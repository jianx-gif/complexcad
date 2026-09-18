import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
wall_thickness = 2.0
chamfer_size = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(outer_radius, wall_thickness + outer_radius)
    .lineTo(outer_radius, wall_thickness + outer_radius)
    .lineTo(outer_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .lineTo(inner_radius, wall_thickness + outer_radius)
    .close()
)
result = outer_radius
