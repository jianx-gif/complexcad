import cadquery as cq
import math

pipe_outer_dia = 20.0
pipe_wall_thk = 2.0
elbow_center_radius = 30.0
fillet_radius = 2.0
hole_dia = 6.0
hole_depth = 10.0
hole_angle_deg = 45.0

pipe_outer_radius = pipe_outer_dia / 2.0
hole_angle_rad = math.radians(hole_angle_deg)
hole_center_x = elbow_center_radius * math.cos(hole_angle_rad)
hole_center_z = elbow_center_radius * math.sin(hole_angle_rad)

path = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .threePointArc((elbow_center_radius, 0), (elbow_center_radius, elbow_center_radius))
    .wire()
)

outer_profile = cq.Workplane("XY").circle(pipe_outer_radius)
outer_solid = outer_profile.sweep(path, multisection=False)

hollow_elbow = outer_solid.shell(-pipe_wall_thk)

filleted_elbow = hollow_elbow.edges().fillet(fillet_radius)

hole_cylinder = (
    cq.Workplane("XZ")
    .center(hole_center_x, hole_center_z)
    .circle(hole_dia / 2.0)
    .extrude(hole_depth)
)

result = filleted_elbow.cut(hole_cylinder)
