import cadquery as cq
import math

pipe_centerline_radius = 30.0
pipe_outer_radius = 8.0
pipe_wall_thickness = 2.0
pipe_inner_radius = pipe_outer_radius - pipe_wall_thickness
elbow_angle_deg = 90.0
access_width = 20.0
access_height = 8.0
access_depth = pipe_outer_radius * 2.0
access_center_angle_deg = 45.0
access_chamfer = 0.5
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
edge_fillet = 0.75

start_pt = (pipe_centerline_radius, 0)
mid_pt = (0, 0)
end_pt = (0, pipe_centerline_radius)
path = (
    cq.Workplane("XZ")
    .moveTo(*start_pt)
    .threePointArc(mid_pt, end_pt)
    .wire()
)

elbow = (
    cq.Workplane("XY")
    .circle(pipe_outer_radius)
    .circle(pipe_inner_radius)
    .sweep(path, makeSolid=True, isFrenet=True)
)

access_angle_rad = math.radians(access_center_angle_deg)
access_center_x = pipe_centerline_radius * math.cos(access_angle_rad)
access_center_z = pipe_centerline_radius * math.sin(access_angle_rad)
access_box = (
    cq.Workplane("XY")
    .box(access_width, access_height, access_depth)
    .translate((access_center_x, 0, access_center_z))
    .rotate((0, 0, 0), (0, 1, 0), -access_center_angle_deg)
)

elbow = elbow.cut(access_box)
elbow = elbow.edges("|Z").chamfer(access_chamfer)

inlet_face = elbow.faces(">X").workplane()
hole_positions = [(0, mount_hole_offset), (0, -mount_hole_offset)]
elbow = inlet_face.pushPoints(hole_positions).hole(mount_hole_diameter)

elbow = elbow.edges("|Z").fillet(edge_fillet)

result = elbow