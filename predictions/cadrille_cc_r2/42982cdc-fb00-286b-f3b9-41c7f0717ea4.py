import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
height = 12.0
fillet_radius = 0.5
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(height)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(height)
)
result = base.cut(inner_cyl)
result = result.edges().fillet(fillet_radius)
result = result.faces(">Z").edges().chamfer(chamfer_distance)
result = result.faces(">Z").edges().fillet(fillet_radius)
