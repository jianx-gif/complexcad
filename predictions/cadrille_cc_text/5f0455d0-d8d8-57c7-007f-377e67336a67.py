import cadquery as cq
pipe_outer_radius = 8.0
pipe_wall_thickness = 1.5
pipe_angle_deg = 45.0
chamfer_size = 0.8
flange_length = 12.0
flange_width = 30.0
boss_width = 10.0
boss_height = 6.0
bolt_hole_dia = 2.0
bolt_hole_pitch = 10.0
bolt_angle_rad = math.radians(boss_angle_deg)
bolt_angle_rad = math.radians(boss_angle_rad)
base = (
    cq.Workplane("XY")
    .moveTo(pipe_outer_radius, 0)
    .lineTo(pipe_outer_radius, pipe_wall_thickness)
    .lineTo(pipe_outer_radius + pipe_wall_thickness, pipe_wall_thickness)
    .lineTo(pipe_outer_radius + pipe_wall_thickness, pipe_wall_thickness + boss_height)
    .lineTo(pipe_outer_radius + boss_width, pipe_wall_thickness + boss_height)
    .lineTo(pipe_outer_radius, pipe_wall_thickness + boss_height)
    .lineTo(pipe_outer_radius, 0)
    .close()
    .extrude(boss_width)
)
boss = (
    cq.Workplane("XY")
    .circle(boss_width / 2)
    .extrude(boss_height)
    .translate((0, 0, boss_width))
)
result = base.union(boss)
result = result.edges("|Z").chamfer(chamfer_size)
result = result.edges("|Z").chamfer(chamfer_size)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(bolt_angle_rad, 0)
    .hole(bolt_hole_dia)
)
