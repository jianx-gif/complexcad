import cadquery as cq

pipe_outer_radius = 25.0
pipe_wall_thickness = 3.0
pipe_length = 80.0
step_reduction = 5.0
step_length = 30.0
clearance_hole_dia = 4.0
chamfer_dist = 0.5
fillet_radius = 1.0

pipe_inner_radius = pipe_outer_radius - pipe_wall_thickness
step_inner_radius = pipe_inner_radius - step_reduction

profile = (
    cq.Workplane('XZ')
    .moveTo(pipe_outer_radius, 0)
    .lineTo(pipe_outer_radius, pipe_length)
    .lineTo(pipe_inner_radius, pipe_length)
    .lineTo(pipe_inner_radius, pipe_length - step_length)
    .lineTo(step_inner_radius, pipe_length - step_length)
    .lineTo(step_inner_radius, 0)
    .close()
)

solid = profile.revolve()

hole = (
    cq.Workplane('YZ')
    .center(0, pipe_length/2)
    .circle(clearance_hole_dia/2)
    .extrude(pipe_outer_radius*2 + 1)
)

result = (
    solid
    .cut(hole)
    .edges('<Z')
    .chamfer(chamfer_dist)
    .edges('>Z')
    .fillet(fillet_radius)
)
