import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
height = 20.0
wall_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 8
hole_radius = outer_radius - wall_thickness
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
result = base.cut(inner_cyl)
result = result.edges().chamfer(chamfer_distance)
result = (
    result.faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutBlind(-hole_count)
)
result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutBlind(-hole_count)
)
