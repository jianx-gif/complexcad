import cadquery as cq

# parameters
base_radius = 30.0
base_height = 5.0
groove_depth = 5.0
groove_height = 0.5
frame_width = 50.0
frame_depth = 30.0
frame_height = 8.0
frame_recess_depth = 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 8.0
hole_count = 8

# base profile for revolve (includes a small radial groove)
base_profile = (
    cq.Workplane("XZ")
    .lineTo(0, base_height)  # vertical up
    .lineTo(base_radius, base_height)  # radial out
    .lineTo(base_radius, base_height + groove_height)  # small vertical up for groove
    .lineTo(base_radius - groove_depth, base_height + groove_height)  # inward to create groove width
    .lineTo(base_radius - groove_depth, base_height)  # down back to main height
    .lineTo(0, base_height)  # back to axis
    .close()
)

# revolve the profile to create cylindrical base
base = base_profile.revolve()

# add raised rectangular frame on top of base
frame = (
    base
    .faces(">Z")
    .workplane()
    .rect(frame_width, frame_depth)
    .extrude(frame_height, combine=True)
)

# create a shallow recess on the top surface of the frame
frame_with_recess = (
    frame
    .faces(">Z")
    .workplane()
    .rect(frame_width - 2 * frame_recess_depth, frame_depth - 2 * frame_recess_depth)
    .cutBlind(-frame_recess_depth)
)

# apply chamfer to top edges of the raised frame
chamfered = frame_with_recess.edges("|Z").chamfer(chamfer_size)

# create linear array of eight M4 holes on the top face
# calculate x positions centered
half_span = (hole_count - 1) * hole_spacing / 2.0
hole_positions = [(-half_span + i * hole_spacing, 0) for i in range(hole_count)]

result = (
    chamfered
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
