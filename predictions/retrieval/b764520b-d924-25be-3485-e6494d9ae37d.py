import cadquery as cq

main_diameter = 30
wall_thickness = 4
main_length = 80
branch_diameter = 20
branch_length = 50
groove_width = 10
groove_depth = 2
groove_center_z = main_length/2
fillet_radius = 2
boss_diameter = 15
boss_height = 12
boss_center_z = main_length*0.3
tap_thread_diam = 6

main_outer = main_diameter/2
main_inner = main_outer - wall_thickness
branch_outer = branch_diameter/2
branch_inner = branch_outer - wall_thickness

main_pipe = (
    cq.Workplane('XY')
    .circle(main_outer)
    .circle(main_inner)
    .extrude(main_length)
)

branch_pipe = (
    cq.Workplane('YZ')
    .circle(branch_outer)
    .circle(branch_inner)
    .extrude(branch_length)
    .translate((0, 0, main_length/2))
)

groove_cut = (
    cq.Workplane('XY')
    .center(main_outer - groove_depth/2, 0)
    .circle(groove_depth/2)
    .extrude(groove_width)
    .translate((0, 0, groove_center_z - groove_width/2))
)

boss = (
    cq.Workplane('YZ')
    .center(0, boss_center_z)
    .circle(boss_diameter/2)
    .extrude(boss_height)
    .translate((main_outer, 0, 0))
)

boss = boss.edges().fillet(fillet_radius)

# Tapped hole in boss, blind hole depth equal to boss height
tap_hole = (
    cq.Workplane('YZ')
    .center(0, boss_center_z)
    .circle(tap_thread_diam/2)
    .extrude(-boss_height)
    .translate((main_outer + boss_height, 0, 0))
)

combined = main_pipe.union(branch_pipe).union(boss)
combined = combined.cut(groove_cut)
combined = combined.cut(tap_hole)
result = combined
