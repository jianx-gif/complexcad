import cadquery as cq

# Parameters
bracket_radius = 30
bracket_length = 50
shoulder_height = 12
shoulder_radius = 20
blind_hole_diameter = 10
blind_hole_depth = 30
thread_pitch = 4
thread_major_dia = 28
thread_length = 20
thread_tri_height = thread_pitch * 0.6
slot_width = 12
slot_height = 6
slot_offset = 15

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane('XZ')
    .moveTo(bracket_radius, 0)
    .lineTo(bracket_radius, bracket_length - shoulder_height)
    .lineTo(shoulder_radius, bracket_length - shoulder_height)
    .lineTo(shoulder_radius, bracket_length)
    .lineTo(0, bracket_length)
    .close()
)

body = profile.revolve()

slot = (
    cq.Workplane('YZ')
    .workplane(offset=slot_offset)
    .center(0, bracket_length/2)
    .rect(slot_width, slot_height)
    .extrude(bracket_radius*2, combine=False)
)
body = body.cut(slot)

hole = (
    cq.Workplane('XY')
    .center(0, 0)
    .circle(blind_hole_diameter/2)
    .extrude(-blind_hole_depth)
)
body = body.cut(hole)

thread_radius = bracket_radius + thread_tri_height/2
helix_wire = cq.Wire.makeHelix(pitch=thread_pitch, height=thread_length, radius=thread_radius)
helix_wire = helix_wire.translate((0, 0, bracket_length - thread_length))
tri_profile = (
    cq.Workplane('XY')
    .polyline([
        (0, 0),
        (thread_tri_height/2, thread_pitch/2),
        (thread_tri_height, 0),
        (0, 0)
    ])
    .close()
)
thread = tri_profile.sweep(helix_wire, multisection=True)
body = body.union(thread)

result = body
