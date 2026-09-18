import cadquery as cq

body_diameter = 60.0
body_length = 80.0
shoulder_diameter = 80.0
shoulder_length = 20.0
wall_thickness = 4.0
fillet_radius = 6.0
chamfer_size = 2.0
inlet_diameter = 20.0
inlet_angle = 45.0
inlet_depth = 30.0
exhaust_diameter = 30.0
exhaust_length = 15.0
thread_pitch = 5.0
thread_depth = 2.0
thread_length = 12.0
mount_hole_diameter = 6.0
mount_pattern_radius = 30.0
mount_hole_count = 4

outer_radius_body = body_diameter / 2.0
outer_radius_shoulder = shoulder_diameter / 2.0
step_z = body_length - shoulder_length - fillet_radius

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius_body, 0)
    .lineTo(outer_radius_body, step_z)
    .radiusArc((outer_radius_shoulder, step_z + fillet_radius), fillet_radius)
    .lineTo(outer_radius_shoulder, body_length)
    .lineTo(0, body_length)
    .close()
)

body = profile.revolve()

body = (
    body.shell(-wall_thickness)
    .edges("<Z")
    .chamfer(chamfer_size)
)

inlet_cyl = (
    cq.Workplane("XY")
    .circle(inlet_diameter / 2.0)
    .extrude(inlet_depth)
    .rotate((0, 0, 0), (0, 0, 1), inlet_angle)
    .translate((outer_radius_body - wall_thickness / 2.0, 0, body_length / 2.0))
)

body = body.cut(inlet_cyl)

exhaust_cyl = (
    cq.Workplane("XY")
    .circle(exhaust_diameter / 2.0)
    .extrude(exhaust_length)
    .translate((0, 0, body_length))
)

body = body.union(exhaust_cyl)

thread_angle = 360.0 * thread_length / thread_pitch
thread_profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (thread_pitch / 2.0, thread_depth),
        (thread_pitch, 0)
    ])
    .close()
)

thread_solid = (
    thread_profile
    .twistExtrude(thread_length, thread_angle, combine=False)
    .translate((exhaust_diameter / 2.0 + thread_depth / 2.0, 0, body_length))
)

body = body.cut(thread_solid)

mount_hole = (
    cq.Workplane("XY")
    .circle(mount_hole_diameter / 2.0)
    .extrude(body_length)
    .translate((mount_pattern_radius, 0, body_length / 2.0))
)

for i in range(mount_hole_count):
    angle = i * 360.0 / mount_hole_count
    rotated_hole = mount_hole.rotate((0, 0, 0), (0, 0, 1), angle)
    body = body.cut(rotated_hole)

result = body