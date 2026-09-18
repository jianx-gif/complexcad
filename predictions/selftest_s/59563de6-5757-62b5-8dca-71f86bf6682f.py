import cadquery as cq

coupler_length = 60.0
major_dia = 30.0
major_radius = major_dia / 2.0
thread_pitch = 4.0
thread_depth = 0.6 * thread_pitch
minor_radius = major_radius - thread_depth
chamfer_len = 5.0
inner_dia = 20.0
inner_radius = inner_dia / 2.0
relief_groove_width = 3.0
relief_groove_depth = 2.0
relief_groove_position = coupler_length * 0.4
thread_length = coupler_length - chamfer_len
thread_height = thread_pitch

# Base body profile and revolve
base_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(minor_radius - chamfer_len, chamfer_len)
    .lineTo(minor_radius, chamfer_len)
    .lineTo(minor_radius, coupler_length)
    .lineTo(0, coupler_length)
    .close()
)
base_body = base_profile.revolve()

# Inner bore cut
bore = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(inner_radius)
    .extrude(coupler_length)
)
result = base_body.cut(bore)

# Relief groove cut (axial ring)
relief = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(inner_radius + relief_groove_depth)
    .extrude(relief_groove_width)
    .translate((0, 0, relief_groove_position - relief_groove_width / 2))
)
result = result.cut(relief)

# Thread profile triangle
thread_profile = (
    cq.Workplane("XZ")
    .moveTo(minor_radius, 0)
    .lineTo(major_radius, thread_height / 2)
    .lineTo(minor_radius, thread_height)
    .close()
)
# Helix wire for thread sweep
helix_wire = cq.Wire.makeHelix(pitch=thread_pitch, height=thread_length, radius=(minor_radius + major_radius) / 2.0)
thread_solid = thread_profile.sweep(helix_wire)
result = result.union(thread_solid)
