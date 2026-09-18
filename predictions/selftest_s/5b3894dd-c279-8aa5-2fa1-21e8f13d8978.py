import cadquery as cq
outer_radius = 35
inner_radius_step1 = 20
inner_radius_step2 = 15
block_height = 60
step_start = 20
step_height = 15
hole_diameter = 4
hole_center_radius = 24
outer_chamfer = 1.0
profile = (cq.Workplane('XY')
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, step_start)
    .lineTo(inner_radius_step1, step_start)
    .lineTo(inner_radius_step1, step_start + step_height)
    .lineTo(inner_radius_step2, step_start + step_height)
    .lineTo(inner_radius_step2, block_height)
    .lineTo(0, block_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(outer_chamfer)
holes = (cq.Workplane('XY')
    .polarArray(6, 0, 60, hole_center_radius)
    .circle(hole_diameter/2)
    .extrude(block_height+2)
)
result = solid.cut(holes)
