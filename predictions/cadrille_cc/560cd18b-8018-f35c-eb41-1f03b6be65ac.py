import cadquery as cq
base_length = 80.0
base_width = 60.0
base_thickness = 8.0
frame_outer_radius = 40.0
frame_inner_radius = 20.0
frame_height = 6.0
frame_wall_thickness = 4.0
frame_wall_thickness = 6.0
frame_height = 3.0
frame_chamfer = 1.0
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
    .extrude(frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_inner_radius - frame_wall_thickness/2, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_inner_radius - frame_wall_thickness/2, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_inner_radius - frame_wall_thickness/2, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_inner_radius - frame_wall_thickness/2, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .center(frame_inner_radius - frame_wall_thickness/2, 0)
    .rect(frame_inner_radius, frame_inner_radius)
    .cutBlind(-frame_height)
)
result = frame
