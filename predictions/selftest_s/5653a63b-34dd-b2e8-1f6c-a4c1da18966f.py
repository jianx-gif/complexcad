import cadquery as cq

hole_radius = 12.0
boss_top_radius = 20.0
boss_height = 25.0
spacer_height = 40.0
outer_radius = 45.0
groove_width = 10.0
groove_depth = 5.0
chamfer_size = 1.5
overall_height = boss_height + spacer_height

groove_center_z = overall_height / 2.0

base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(hole_radius, 0)
    .lineTo(hole_radius, boss_height)
    .lineTo(boss_top_radius, boss_height)
    .lineTo(boss_top_radius, boss_height + spacer_height)
    .lineTo(outer_radius, boss_height + spacer_height)
    .lineTo(outer_radius, 0)
    .close()
    .revolve()
)

groove_cutter = (
    cq.Workplane("XY")
    .center(0, 0)
    .cylinder(groove_width, outer_radius - groove_depth)
    .translate((0, 0, groove_center_z - groove_width / 2.0))
)

result = (
    base
    .cut(groove_cutter)
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
    .faces("<Z")
    .edges()
    .chamfer(chamfer_size)
)
