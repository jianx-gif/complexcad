import cadquery as cq
outer_radius = 45
inner_radius = 20
wall_thickness = 2
inner_radius = outer_radius - inner_radius
fillet_radius = 2
chamfer_distance = 1
hole_diameter = 4
hole_spacing = 15
hole_offset = 10
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
result = base.cut(inner_cyl)
result = result.edges().fillet(fillet_radius)
result = result.faces(">Z").edges().chamfer(chamfer_distance)
result = result.faces(">Z").edges().fillet(fillet_radius)
