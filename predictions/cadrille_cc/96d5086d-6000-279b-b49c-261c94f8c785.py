import cadquery as cq
base_length = 100.0
base_width = 30.0
base_thickness = 10.0
frame_outer_radius = 12.0
frame_inner_radius = 25.0
frame_height = 8.0
frame_wall_thickness = 4.0
frame_wall_height = 6.0
frame_height = 6.0
frame_chamfer = 0.5
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
    .rect(frame_outer_radius, frame_outer_radius)
    .extrude(frame_height)
)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().chamfer(frame_chamfer)
frame = (
    frame.faces(">Z").workplane()
    .rarray(frame_wall_thickness, 0, 2, 1)
    .hole(frame_wall_thickness)
)
result = frame
