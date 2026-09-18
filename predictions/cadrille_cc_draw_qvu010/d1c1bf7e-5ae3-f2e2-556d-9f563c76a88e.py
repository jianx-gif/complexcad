import cadquery as cq
outer_diameter = 30.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0 - wall_thickness)
    .lineTo(outer_diameter / 2.0 + wall_thickness, outer_diameter / 2.0 - wall_thickness)
    .lineTo(outer_diameter / 2.0 + wall_thickness, outer_diameter / 2.0 - wall_thickness)
    .lineTo(outer_diameter / 2.0 + wall_thickness, outer_diameter / 2.0 - wall_thickness)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0 - wall_thickness)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(0, outer_diameter / 2.0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
result = solid
