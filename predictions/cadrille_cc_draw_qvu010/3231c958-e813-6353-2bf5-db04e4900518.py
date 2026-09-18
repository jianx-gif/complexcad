import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_depth = thickness * 0.8
hole_count = 6 * hole_diameter
hole_circle_radius = outer_diameter/2 - 5.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter/2, 0)
    .lineTo(inner_diameter/2, thickness)
    .lineTo(inner_diameter/2, thickness + thickness)
    .lineTo(inner_diameter/2, thickness + thickness + thickness)
    .lineTo(inner_diameter/2, thickness + thickness + thickness + thickness)
    .lineTo(inner_diameter/2, thickness + thickness + thickness + thickness)
    .lineTo(inner_diameter/2, thickness + thickness + thickness)
    .lineTo(inner_diameter/2, thickness + thickness + thickness)
    .lineTo(inner_diameter/2, thickness + thickness + thickness)
    .lineTo(inner_diameter/2, thickness + thickness + thickness)
    .lineTo(inner_diameter/2, thickness + thickness + thickness)
    .lineTo(inner_diameter/2, thickness + thickness + thickness)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.edges().chamfer(chamfer_distance)
result = solid
