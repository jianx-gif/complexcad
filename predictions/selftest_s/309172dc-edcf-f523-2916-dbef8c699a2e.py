import cadquery as cq

circle_radius = 20.0
square_side = 35.0
loft_height = 60.0
wall_thickness = 2.0
rib_thickness = 3.0
rib_width = 8.0
rib_spacing = 20.0
fillet_radius = 1.5
chamfer_size = 0.5

outer_loft = (
    cq.Workplane("XY")
    .circle(circle_radius)
    .workplane(offset=loft_height)
    .rect(square_side, square_side)
    .loft()
)
inner_circle_radius = circle_radius - wall_thickness
inner_square_side = square_side - 2 * wall_thickness
inner_loft = (
    cq.Workplane("XY")
    .circle(inner_circle_radius)
    .workplane(offset=loft_height)
    .rect(inner_square_side, inner_square_side)
    .loft()
)
shell_body = outer_loft.cut(inner_loft)
rib_one = (
    cq.Workplane("XY")
    .center(rib_spacing / 2, 0)
    .rect(rib_width, loft_height - 2 * wall_thickness)
    .extrude(rib_thickness)
)
rib_two = (
    cq.Workplane("XY")
    .center(-rib_spacing / 2, 0)
    .rect(rib_width, loft_height - 2 * wall_thickness)
    .extrude(rib_thickness)
)
combined = shell_body.union(rib_one).union(rib_two)
filleted = combined.edges("|Z").fillet(fillet_radius)
result = filleted.edges("|X").chamfer(chamfer_size)
