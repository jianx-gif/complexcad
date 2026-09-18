import cadquery as cq
import math
pipe_outer_dia = 20.0
pipe_wall_thk = 2.0
pipe_inner_dia = pipe_outer_dia - 2 * pipe_wall_thk
elbow_angle_deg = 30.0
elbow_angle_rad = math.radians(elbow_angle_deg)
centerline_radius = 30.0
outer_radius = centerline_radius + pipe_outer_dia / 2.0
inner_radius = centerline_radius - pipe_outer_dia / 2.0
chamfer_dist = 0.5
hole_dia = 4.0
hole_depth = pipe_wall_thk + 1.0
hole_angles = [elbow_angle_rad * 0.25, elbow_angle_rad * 0.5, elbow_angle_rad * 0.75]
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(inner_radius, 0)
    .radiusArc((inner_radius * math.cos(elbow_angle_rad), inner_radius * math.sin(elbow_angle_rad)), inner_radius)
    .lineTo(outer_radius * math.cos(elbow_angle_rad), outer_radius * math.sin(elbow_angle_rad))
    .radiusArc((outer_radius, 0), outer_radius)
    .close()
)
elbow = profile.revolve(elbow_angle_deg)
elbow = elbow.edges(">X").chamfer(chamfer_dist)
result = elbow
for ang in hole_angles:
    x = outer_radius * math.cos(ang)
    y = outer_radius * math.sin(ang)
    hole = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(hole_dia / 2.0)
        .extrude(-hole_depth)
    )
    result = result.cut(hole)
