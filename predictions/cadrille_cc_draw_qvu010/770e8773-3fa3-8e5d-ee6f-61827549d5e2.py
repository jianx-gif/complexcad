import cadquery as cq
outer_diameter = 20.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = inner_radius + wall_thickness / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(