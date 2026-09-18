import cadquery as cq
outer_radius = 10.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(outer_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + hole_spacing
    .lineTo(outer_radius, wall_thickness + wall_thickness + wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + wall_thickness + hole_spacing)
    .lineTo(outer_radius, wall_thickness + hole_spacing)
    .close()
)
result = (
    profile
    .revolve()
    .edges()
    .chamfer(chamfer_size)
)
