import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 80
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
base_thickness = 5
base_height = 30
chamfer_size = 1
hole_diameter = 4
hole_spacing = 12
hole_count = 4
hole_spacing = 12
hole_offset = 10
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
result = result.edges().chamfer(chamfer_size)
result = result.faces(">Z").edges().chamfer(chamfer_size)
result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutBlind(-hole_spacing)
)
result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutBlind(-hole_spacing)
)
