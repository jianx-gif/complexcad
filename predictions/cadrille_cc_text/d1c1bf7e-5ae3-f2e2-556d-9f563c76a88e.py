import cadquery as cq
clamp_body_length = 60.0
total_diameter = 30.0
wall_thickness = 4.0
chamfer = 1.5
set_screw_hole_dia = 4.0
set_screw_spacing = 10.0
set_screw_hole_count = 6
set_screw_offset = total_diameter / 2.0
inner_diameter = clamp_body_length - 2 * wall_thickness
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .polyline([
        (inner_radius, 0),
        (inner_radius, clamp_body_length),
        (inner_radius + clamp_body_length, clamp_body_length),
        (inner_radius + clamp_body_length, total_diameter),
        (inner_radius, total_diameter),
        (inner_radius, 0),
    ])
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer)
set_screw = (
    cq.Workplane("XY")
    .circle(set_screw_hole_dia / 2.0)
    .extrude(total_diameter / 2.0)
)
solid = solid.cut(set_screw)
solid = solid.edges().chamfer(chamfer)
solid = solid.faces(">Z").edges().chamfer(chamfer)
result = solid
