import cadquery as cq
import math
pipe_outer_radius = 8.0
pipe_wall_thickness = 1.5
pipe_inner_radius = pipe_outer_radius - pipe_wall_thickness
elbow_center_radius = 20.0
elbow_angle_deg = 45.0
chamfer_size = 0.8
flange_length = 12.0
flange_width = 30.0
bolt_hole_dia = 2.0
bolt_hole_pitch = 10.0
boss_width = 10.0
boss_height = 6.0
boss_length = 5.0
num_arc_segments = 20
points = []
for i in range(num_arc_segments + 1):
    angle = math.radians(i * elbow_angle_deg / num_arc_segments)
    x = elbow_center_radius * math.cos(angle)
    y = elbow_center_radius * math.sin(angle)
    points.append((x, y, 0))
path = cq.Workplane("XY").spline(points)
pipe = (
    cq.Workplane("XY")
    .circle(pipe_outer_radius)
    .circle(pipe_inner_radius)
    .sweep(path)
)
flange = (
    pipe.faces(">X")
    .workplane(invert=True)
    .rect(flange_width, pipe_outer_radius * 2)
    .extrude(flange_length)
)
pipe = pipe.union(flange)
pipe = pipe.faces(">X").edges().chamfer(chamfer_size)
bolt_grid = [(-bolt_hole_pitch/2, -bolt_hole_pitch/2),
             ( bolt_hole_pitch/2, -bolt_hole_pitch/2),
             (-bolt_hole_pitch/2,  bolt_hole_pitch/2),
             ( bolt_hole_pitch/2,  bolt_hole_pitch/2)]
pipe = (
    pipe.faces(">X")
    .workplane()
    .pushPoints(bolt_grid)
    .hole(bolt_hole_dia)
)
boss = (
    pipe.faces(">X")
    .workplane()
    .rect(boss_width, boss_height)
    .extrude(boss_length)
)
pipe = pipe.union(boss)
result = pipe