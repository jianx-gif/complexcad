import cadquery as cq
import math

pipe_outer_dia = 20.0
pipe_wall_thk = 2.0
pipe_inner_dia = pipe_outer_dia - 2 * pipe_wall_thk
elbow_center_radius = 30.0
elbow_angle_deg = 90.0
chamfer_dist = 0.5
hole_dia = 4.0
hole_depth = pipe_wall_thk + 1.0
hole_count = 4
hole_angle_start = 15.0
hole_angle_step = (elbow_angle_deg - 30.0) / (hole_count - 1)

outer_profile = cq.Workplane("XY").circle(pipe_outer_dia / 2.0)
inner_profile = cq.Workplane("XY").circle(pipe_inner_dia / 2.0)

path = (
    cq.Workplane("XZ")
    .moveTo(elbow_center_radius, 0)
    .radiusArc((0, elbow_center_radius), elbow_center_radius)
)

outer_sweep = outer_profile.sweep(path)
inner_sweep = inner_profile.sweep(path)

elbow = outer_sweep.cut(inner_sweep)

elbow = elbow.edges().chamfer(chamfer_dist)

result = elbow

for i in range(hole_count):
    angle_deg = hole_angle_start + i * hole_angle_step
    angle_rad = math.radians(angle_deg)
    radial_dist = elbow_center_radius + pipe_outer_dia / 2.0 - hole_depth / 2.0
    x = radial_dist * math.cos(angle_rad)
    z = radial_dist * math.sin(angle_rad)
    hole = (
        cq.Workplane("XY")
        .circle(hole_dia / 2.0)
        .extrude(hole_depth)
        .rotate((0, 0, 0), (0, 1, 0), 90)
        .rotate((0, 0, 0), (0, 0, 1), angle_deg)
        .translate((x, 0, z))
    )
    result = result.cut(hole)
