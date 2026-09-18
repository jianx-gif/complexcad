import cadquery as cq
outer_diameter = 80.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_count = 6
hole_radius = inner_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + radi
result = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + radi
    .circle(inner_radius)
    .cutBlind(inner_diameter)
)
