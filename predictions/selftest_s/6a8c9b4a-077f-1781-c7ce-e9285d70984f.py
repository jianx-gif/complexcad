import cadquery as cq
import math
# Parameters
outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
pulley_thickness = 20.0
shell_thickness = 4.0
bearing_seat_radius = 15.0
bearing_seat_depth = 10.0
v_groove_depth = 6.0
hole_diameter = 5.0
hole_depth = 15.0
hole_pitch_radius = 30.0
num_holes = 4
chamfer_size = 0.5
pocket_width = 12.0
pocket_height = 6.0
pocket_depth = 2.0
# Base cylinder and shell
base = (cq.Workplane('XY')
        .circle(outer_radius)
        .extrude(pulley_thickness)
        .shell(shell_thickness))
# Bearing seat cut on back face (-Z)
base = (base.faces('<Z')
        .workplane()
        .circle(bearing_seat_radius)
        .extrude(-bearing_seat_depth))
# V-groove cut using revolved triangular profile
mid_z = pulley_thickness / 2.0
v_half = v_groove_depth / 2.0
tri_points = [
    (outer_radius, mid_z - v_half),
    (outer_radius - v_groove_depth, mid_z),
    (outer_radius, mid_z + v_half)
]
vgroove = (cq.Workplane('XZ')
           .polyline(tri_points)
           .close()
           .revolve(360, (0, 0, 0), (0, 0, 1)))
base = base.cut(vgroove)
# Create pocket solid on front face and chamfer its top edges
pocket = (cq.Workplane('XY')
          .workplane(offset=pulley_thickness)
          .rect(pocket_width, pocket_height)
          .extrude(-pocket_depth))
# Chamfer the top edges of the pocket (edges on top face)
pocket = pocket.edges().chamfer(chamfer_size)
# Cut pocket from base
base = base.cut(pocket)
# Threaded holes on front face (+Z)
angle_step = 360.0 / num_holes
hole_positions = []
for i in range(num_holes):
    ang = math.radians(i * angle_step)
    x = hole_pitch_radius * math.cos(ang)
    y = hole_pitch_radius * math.sin(ang)
    hole_positions.append((x, y))
base = (base.workplane(offset=pulley_thickness)
        .pushPoints(hole_positions)
        .hole(hole_diameter, depth=hole_depth))
result = base
