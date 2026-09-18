import cadquery as cq
import math
elbow_angle = 120
centerline_radius = 30.0
pipe_outer_dia = 20.0
pipe_wall_thickness = 2.0
pipe_inner_dia = pipe_outer_dia - 2 * pipe_wall_thickness
outer_radius = centerline_radius + pipe_outer_dia / 2.0
inner_radius = centerline_radius - pipe_outer_dia / 2.0
fillet_radius = 2.0
boss_dia = 12.0
boss_height = 8.0
boss_hole_dia = 4.0
boss_hole_spacing = 10.0
rib_width = 4.0
rib_height = 6.0
rib_thickness = 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, pipe_outer_dia)
    .threePointArc((outer_radius, pipe_outer_dia + fillet_radius), (outer_radius - fillet_radius, pipe_outer_dia + fillet_radius))
    .lineTo(inner_radius + fillet_radius, pipe_outer_dia + fillet_radius)
    .threePointArc((inner_radius, pipe_outer_dia + fillet_radius), (inner_radius, pipe_outer_dia))
    .lineTo(inner_radius, 0)
    .close()
)
elbow = profile.revolve(elbow_angle)
mid_angle = elbow_angle / 2.0
mid_rad = math.radians(mid_angle)
boss_center_x = (centerline_radius + pipe_outer_dia / 2.0) * math.cos(mid_rad)
boss_center_z = (centerline_radius + pipe_outer_dia / 2.0) * math.sin(mid_rad)
boss = (
    cq.Workplane("XZ")
    .center(boss_center_x, boss_center_z)
    .circle(boss_dia / 2.0)
    .extrude(boss_height)
)
boss = (
    boss.faces(">Y")
    .workplane()
    .pushPoints([(-boss_hole_spacing / 2.0, 0), (boss_hole_spacing / 2.0, 0)])
    .hole(boss_hole_dia)
)
rib = (
    cq.Workplane("XZ")
    .center(boss_center_x, boss_center_z)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
result = elbow.union(boss).union(rib)
