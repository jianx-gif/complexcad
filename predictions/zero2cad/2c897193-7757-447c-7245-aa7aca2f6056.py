import cadquery as cq
import math

pipe_outer_dia = 20.0
pipe_wall_thk = 2.5
pipe_inner_dia = pipe_outer_dia - 2 * pipe_wall_thk
elbow_center_radius = 30.0
chamfer_dist = 0.5
hole_dia = 5.0
hole_count = 4
hole_angle_offset = 15.0

path = (
    cq.Workplane("XZ")
    .moveTo(elbow_center_radius, 0)
    .threePointArc((0, 0), (0, elbow_center_radius))
    .wire()
)

outer_profile = cq.Workplane("YZ").circle(pipe_outer_dia / 2)
outer_sweep = outer_profile.sweep(path, multisection=False)

inner_profile = cq.Workplane("YZ").circle(pipe_inner_dia / 2)
inner_sweep = inner_profile.sweep(path, multisection=False)

elbow = outer_sweep.cut(inner_sweep)

elbow = elbow.edges("|Z").chamfer(chamfer_dist)

hole_radius = pipe_outer_dia / 2 - pipe_wall_thk / 2
hole_positions = []
for i in range(hole_count):
    angle = math.radians(hole_angle_offset + i * 360.0 / hole_count)
    x = hole_radius * math.cos(angle)
    z = hole_radius * math.sin(angle)
    hole_positions.append((x, z))

result = (
    elbow
    .faces(">Y")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_dia)
)
