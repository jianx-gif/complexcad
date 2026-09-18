import cadquery as cq
outer_radius = 45
inner_radius = 20
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
base_thickness = 10
base_height = 30
chamfer_distance = 2
hole_diameter = 5
hole_spacing = 15
hole_count = 6
hole_spacing = 12
chamfer_distance = 2
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base_thickness)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(base_thickness)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(base_thickness)
)
result = base.cut(inner_cyl)
result = result.edges().chamfer(chamfer_distance)
result = result.faces(">Z").workplane().hole(hole_diameter)
result = result.faces(">Z").edges().chamfer(chamfer_distance)
