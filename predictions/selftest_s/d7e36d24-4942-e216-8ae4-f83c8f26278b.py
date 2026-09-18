import cadquery as cq

# Parameters
body_outer_dia = 60.0
body_inner_dia = 50.0
body_length = 40.0
flange_outer_dia = 80.0
flange_thickness = 5.0
top_flange_thickness = 5.0
boss_dia = 30.0
boss_height = 15.0
thread_dia = 22.0
thread_length = 12.0
chamfer = 1.0
mount_hole_dia = 5.0
mount_spacing = 30.0

# Derived dimensions
flange_outer_radius = flange_outer_dia / 2.0
body_outer_radius = body_outer_dia / 2.0
body_inner_radius = body_inner_dia / 2.0
boss_radius = boss_dia / 2.0
total_height = flange_thickness + body_length + top_flange_thickness

result = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(0, flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness)
    .lineTo(flange_outer_radius, flange_thickness + body_length)
    .lineTo(flange_outer_radius, total_height)
    .lineTo(0, total_height)
    .lineTo(0, total_height - top_flange_thickness)
    .lineTo(body_inner_radius, total_height - top_flange_thickness)
    .lineTo(body_inner_radius, flange_thickness)
    .lineTo(0, flange_thickness)
    .close()
    .revolve()
    .faces('>Z')
    .workplane()
    .circle(boss_radius)
    .extrude(boss_height)
    .faces('>Z')
    .workplane()
    .hole(thread_dia, thread_length)
    .edges()
    .chamfer(chamfer)
    .faces('<Z')
    .workplane()
    .pushPoints([
        (-mount_spacing/2, -mount_spacing/2),
        (-mount_spacing/2, mount_spacing/2),
        (mount_spacing/2, -mount_spacing/2),
        (mount_spacing/2, mount_spacing/2)
    ])
    .hole(mount_hole_dia, flange_thickness)
)
