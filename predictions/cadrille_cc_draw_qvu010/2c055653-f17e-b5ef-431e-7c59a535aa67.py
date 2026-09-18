import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 10.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_depth = thickness * 0.6
hole_count = 6
hole_circle_radius = outer_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .lineTo(inner_diameter / 2.0 - thickness, thickness)
    .