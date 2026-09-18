import cadquery as cq
hole_radius = 12.0
boss_top_radius = 20.0
boss_height = 25.0
spacer_height = 40.0
groove_width = 10.0
groove_depth = 5.0
chamfer_size = 1.5
outer_radius = 45.0
boss_radius = boss_top_radius + boss_height
boss_height = boss_height - 2 * groove_width
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, boss_height)
    .lineTo(boss_radius, boss_height)
    .lineTo(boss_radius, boss_height + boss_height)
    .lineTo(0, boss_height + boss_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
groove = (
    cq.Workplane("XY")
    .center(outer_radius - groove_width / 2, boss_height / 2)
    .circle(groove_width / 2)
    .extrude(groove_depth)
)
solid = solid.cut(groove)
solid = solid.edges().chamfer(chamfer_size)
result = solid
