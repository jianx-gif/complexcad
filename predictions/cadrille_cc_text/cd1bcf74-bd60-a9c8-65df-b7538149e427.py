import cadquery as cq
outer_diameter = 80.0
step_radius = 60.0
step_height = 30.0
thread_diameter = 10.0
thread_length = 15.0
arc_angle_deg = 120.0
mount_hole_diameter = 4.0
mount_hole_radius = 30.0
chamfer_distance = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2, 0)
    .lineTo(outer_diameter / 2, step_height)
    .lineTo(step_radius, step_height)
    .lineTo(step_radius, step_height + step_height)
    .lineTo(step_radius + step_radius, step_height + step_height)
    .lineTo(step_radius, step_height)
    .lineTo(step_radius, 0)
    .close()
)
result = profile.revolve()
result = result.edges().chamfer(chamfer_distance)
result = (
    result.faces(">Z")
    .workplane()
    .hole(thread_diameter, depth=thread_length)
)
result = (
    result.faces(">Z")
    .workplane()
    .hole(thread_diameter, depth=thread_length)
)
result = (
    result.faces(">Z")
    .workplane()
    .hole(mount_hole_diameter, depth=thread_length)
)
result = (
    result.faces(">Z")
    .workplane()
    .hole(mount_hole_diameter, depth=thread_length)
)
