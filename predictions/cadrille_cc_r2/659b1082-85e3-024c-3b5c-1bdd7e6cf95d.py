import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 60
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
base_thickness = 5
base_height = 10
chamfer_distance = 1
hole_diameter = 4
hole_spacing = 15
hole_count = 4
hole_spacing = 12
chamfer_distance = 2
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
result = result.edges().chamfer(chamfer_distance)
result = result.faces(">Z").edges().chamfer(chamfer_distance)
result = result.faces(">Z").edges().chamfer(chamfer_distance)
