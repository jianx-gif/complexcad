import cadquery as cq
base_length = 80.0
base_width = 80.0
base_thickness = 5.0
frame_outer_radius = 30.0
frame_inner_radius = 20.0
frame_height = 8.0
frame_wall_thickness = 2.0
frame_wall_thickness = 4.0
frame_height = 10.0
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
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(frame_wall_thickness)
frame = frame.edges().fillet(fillet_wall_thickness)
frame = frame.edges().filpyLine(fillet_wall_thickness)
frame = frame.edges().filpyLine(fillet_wall_thickness)
frame = frame.edges().filpyLine(fillet_wall_thickness)
frame = frame.faces(">Z").workplane().hole(frame_wall_thickness)
frame = frame.edges().chamfer(frame_chamfer)
frame = frame.faces(">Z").workplane().hole(frame_wall_thickness)
frame = frame.edges().chamfer(frame_chamfer)
frame = frame.faces(">Z").workplane().hole(frame_wall_thickness)
frame = frame.edges().chamfer(frame_chamfer)
frame = frame.faces(">Z").workplane().hole(frame_wall_thickness)
frame = frame.edges().chamfer(frame_chamfer)
frame = frame.faces(">Z").workplane().center(0, 0).hole(frame_wall_thickness)
frame = frame.edges().filpyIn(i, frame)
frame = frame.faces(">Z").workplane().center(0, 0).rect(frame_outer_radius, frame_outer_radius).cutBlind(frame_wall_thickness)
frame = frame.edges().chamfer(frame_chamfer)
result = frame
