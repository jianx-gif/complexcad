import cadquery as cq
outer_radius = 25.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + radi
    )
)
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
    .edges()
    .chamfer(chamfer_distance)
)
