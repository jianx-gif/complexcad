import cadquery as cq

# Parameters
knob_outer_radius = 30.0
knob_height = 45.0
shoulder_radius = 20.0
shoulder_height = 12.0
thread_pitch = 4.0
thread_depth = 2.0
thread_length = 20.0
chamfer_size = 1.0
slot_width = 6.0
slot_height = 12.0
slot_depth = 8.0

# Base knob profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(knob_outer_radius, 0)
    .lineTo(knob_outer_radius, knob_height - shoulder_height)
    .lineTo(shoulder_radius, knob_height - shoulder_height)
    .lineTo(shoulder_radius, knob_height)
    .lineTo(0, knob_height)
    .close()
)
knob_body = profile.revolve()

# Thread profile (triangular) for internal thread
thread_profile = (
    cq.Workplane("XZ")
    .moveTo(shoulder_radius - thread_depth, 0)
    .lineTo(shoulder_radius, thread_pitch / 2)
    .lineTo(shoulder_radius - thread_depth, thread_pitch)
    .close()
)
# Helical path for thread using Wire.makeHelix
helix_path = cq.Wire.makeHelix(pitch=thread_pitch, height=thread_length, radius=shoulder_radius - thread_depth / 2)
thread_solid = thread_profile.sweep(helix_path)
# Cut thread from knob body
knob_with_thread = knob_body.cut(thread_solid)

# Side slot for grip (cut through side)
slot = (
    cq.Workplane("YZ")
    .center(0, knob_height / 2)
    .rect(slot_height, slot_width)
    .extrude(slot_depth)
    .translate((knob_outer_radius - slot_depth / 2, 0, 0))
)
knob_with_slot = knob_with_thread.cut(slot)

# Chamfer top edge
result = knob_with_slot.edges("<<Z[-1]").chamfer(chamfer_size)
