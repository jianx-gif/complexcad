import cadquery as cq
pulley_outer_radius = 45.0
pulley_width = 20.0
groove_depth = 8.0
groove_angle = 45.0
groove_depth = 10.0
set_screw_diameter = 3.0
set_screw_head_diameter = 6.0
set_screw_head_depth = 2.0
set_screw_offset = 7.0
rib_width = 5.0
rib_height = 3.0
rib_length = pulley_width - 2 * rib_width
set_screw_head_diameter = set_screw_diameter - 2 * rib_width
set_screw_head_depth = set_screw_head_diameter - 2 * rib_width
profile = (
    cq.Workplane("XZ")
    .moveTo(pulley_outer_radius, 0)
    .lineTo(pulley_outer_radius, pulley_width)
    .lineTo(pulley_outer_radius, pulley_width + rib_height)
    .lineTo(pulley_outer_radius, pulley_width + rib_height)
    .lineTo(pulley_outer_radius, pulley_width + rib_height)
    .lineTo(pulley_outer_radius, 0)
    .close()
)
result = profile.revolve()
groove = (
    cq.Workplane("XY")
    .circle(groove_depth)
    .extrude(groove_depth)
    .translate((0, 0, pulley_width + groove_depth))
)
result = result.cut(groove)
set_screw = (
    cq.Workplane("XY")
    .circle(set_screw_head_diameter / 2)
    .extrude(set_screw_head_depth)
)
result = result.cut(set_screw)
result = result.edges().chamfer(set_screw_head_depth)
result = result.edges().chamfer(set_screw_head_depth)
