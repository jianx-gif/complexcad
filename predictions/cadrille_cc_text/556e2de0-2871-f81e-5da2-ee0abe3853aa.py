import cadquery as cq
pipe_outer_radius = 10.0
pipe_center_radius = 30.0
pipe_thickness = 2.0
chamfer_distance = 1.0
thread_cavity_diameter = 6.0
thread_cavity_depth = 8.0
boss_width = 12.0
boss_height = 6.0
boss_length = 8.0
boss_offset = pipe_center_radius - pipe_center_radius - boss_width / 2.0
boss = (
    cq.Workplane("XY")
    .moveTo(pipe_center_radius, 0)
    .lineTo(pipe_center_radius, pipe_center_radius)
    .lineTo(pipe_center_radius + pipe_thickness, pipe_center_radius)
    .lineTo(pipe_center_radius + pipe_thickness, pipe_center_radius)
    .lineTo(pipe_center_radius + pipe_thickness, pipe_center_radius)
    .lineTo(pipe_center_radius, pipe_center_radius)
    .close()
    .wire()
)
boss = (
    cq.Workplane("XY")
    .center(pipe_center_radius + boss_offset, pipe_center_radius)
    .circle(boss_width / 2.0)
    .extrude(boss_height)
)
boss = boss.translate((0, 0, pipe_center_radius))
boss = boss.translate((0, 0, pipe_center_radius))
boss = boss.translate((0, 0, pipe_center_radius))
result = boss
