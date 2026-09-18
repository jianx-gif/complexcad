import cadquery as cq
outer_radius = 45
inner_radius = 20
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
fillet_radius = 2
chamfer_distance = 1
hole_diameter = 5
hole_spacing = 30
hole_count = 12
hole_count = 6
hole_spacing = 12
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
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
result = inner_cyl.cut(inner_cyl)
