import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 80
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
base_thickness = 10
base_height = 20
chamfer_size = 1
hole_diameter = 5
hole_spacing = 30
hole_count = 6
hole_count = 4
hole_spacing = 15
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
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(height)
)
result = inner_cyl.cut(inner_cyl)
