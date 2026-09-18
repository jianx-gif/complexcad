import cadquery as cq
base_length = 80.0
base_width = 60.0
base_thickness = 6.0
frame_outer_radius = 30.0
frame_inner_radius = 20.0
frame_height = 8.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness, centered=(True, True, False))
    .edges("|Z").chamfer(chamfer_size)
)
frame = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(frame_outer_radius, frame_outer_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_inner_radius - frame_inner_radius, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_inner_radius - frame_inner_radius, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_inner_radius - frame_inner_radius, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_inner_radius - frame_inner_radius, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
result = frame
