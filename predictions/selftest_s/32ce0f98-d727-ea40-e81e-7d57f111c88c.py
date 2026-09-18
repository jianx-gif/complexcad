import cadquery as cq
import math
pipe_outer_radius = 10.0
pipe_thickness = 2.0
straight_length = 80.0
elbow_center_radius = 30.0
elbow_angle_deg = 45.0
fillet_radius = 0.5
# Straight pipe solid and hollow it
straight_outer = cq.Workplane('XY').circle(pipe_outer_radius).extrude(straight_length)
straight_pipe = straight_outer.shell(-pipe_thickness)
# Elbow path points
mid_angle = elbow_angle_deg / 2.0
mid_rad = math.radians(mid_angle)
final_rad = math.radians(elbow_angle_deg)
mid_x = elbow_center_radius * (1 - math.cos(mid_rad))
mid_z = straight_length + elbow_center_radius * math.sin(mid_rad)
final_x = elbow_center_radius * (1 - math.cos(final_rad))
final_z = straight_length + elbow_center_radius * math.sin(final_rad)
path = (
    cq.Workplane('XY')
    .spline([ (0, 0, straight_length), (mid_x, 0, mid_z), (final_x, 0, final_z) ])
    .wire()
)
outer_elbow = (
    cq.Workplane('XY')
    .transformed(offset=(0, 0, straight_length))
    .circle(pipe_outer_radius)
    .sweep(path)
)
inner_elbow = (
    cq.Workplane('XY')
    .transformed(offset=(0, 0, straight_length))
    .circle(pipe_outer_radius - pipe_thickness)
    .sweep(path)
)
elbow_pipe = outer_elbow.cut(inner_elbow)
elbow_pipe = elbow_pipe.edges().fillet(fillet_radius)
result = straight_pipe.union(elbow_pipe)
