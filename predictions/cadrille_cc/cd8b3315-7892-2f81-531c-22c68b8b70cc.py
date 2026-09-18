import cadquery as cq
base_length = 80.0
base_width = 50.0
base_thickness = 4.0
frame_outer_radius = 30.0
frame_inner_radius = 20.0
frame_height = 8.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
frame = (
    base.faces(">Z").workplane()
    .rect(frame_outer_radius, frame_outer_radius)
    .extrude(frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .rect(frame_outer_radius, frame_outer_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_outer_radius - frame_inner_radius, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_outer_radius - frame_inner_radius, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_outer_radius - frame_inner_radius, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_outer_radius - frame_inner_radius, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
result = frame
