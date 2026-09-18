import cadquery as cq
import math

pipe_inner_radius = 8.0
wall_thickness = 2.0
pipe_outer_radius = pipe_inner_radius + wall_thickness
bend_center_radius = 30.0
elbow_angle_deg = 120.0
chamfer_size = 1.0
hole_diameter = 3.0
hole_depth = wall_thickness + 0.5
num_holes = 6
mount_hole_diameter = 4.0
block_width = 8.0
block_length = 12.0
block_height = 6.0
mount_hole_block_dia = 3.0

outer_profile = cq.Workplane("YZ").circle(pipe_outer_radius).wire()
mid_angle = elbow_angle_deg / 2.0
mid = (bend_center_radius * math.cos(math.radians(mid_angle)), bend_center_radius * math.sin(math.radians(mid_angle)))
end = (bend_center_radius * math.cos(math.radians(elbow_angle_deg)), bend_center_radius * math.sin(math.radians(elbow_angle_deg)))
path = cq.Workplane("XY").moveTo(0, 0).threePointArc(mid, end).wire()
outer_solid = outer_profile.sweep(path)
pipe = outer_solid.shell(-wall_thickness)
pipe = pipe.faces("<X").edges().chamfer(chamfer_size)
angles = [i * elbow_angle_deg / (num_holes - 1) for i in range(num_holes)]
for angle in angles:
    rad = math.radians(angle)
    radial_distance = bend_center_radius + pipe_outer_radius
    x = radial_distance * math.cos(rad)
    y = radial_distance * math.sin(rad)
    hole = (cq.Workplane("YZ")
            .circle(hole_diameter/2)
            .extrude(hole_depth)
            .rotate((0,0,0), (0,0,1), angle)
            .translate((x, y, 0)))
    pipe = pipe.cut(hole)
pipe = pipe.faces("<X").workplane().hole(mount_hole_diameter)
block = (pipe.faces(">X").workplane().rect(block_width, block_length).extrude(block_height))
pipe = pipe.union(block)
pipe = pipe.faces(">X").workplane().hole(mount_hole_block_dia)
result = pipe
