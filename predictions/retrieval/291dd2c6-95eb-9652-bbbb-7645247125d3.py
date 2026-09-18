import cadquery as cq
import math
overall_diameter = 80.0
wall_thickness = 10.0
outer_flange_height = 12.0
inner_rib_height = 6.0
inner_rib_width = 4.0
fillet_radius = 0.5
chamfer_distance = 0.5
pilot_hole_diameter = 4.0
counterbore_diameter = 8.0
counterbore_depth = 8.0
mount_hole_diameter = 3.0
mount_hole_setback = 5.0
num_mount_holes = 4
outer_radius = overall_diameter / 2.0
inner_radius = outer_radius - wall_thickness
# Base cylindrical ring
base_solid = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_flange_height)
    .faces(">Z")
    .workplane()
    .hole(inner_radius * 2)
)
# Rib protrusion
rib_solid = (
    cq.Workplane("XY")
    .center(inner_radius + inner_rib_width / 2.0, 0)
    .rect(inner_rib_width, inner_rib_height)
    .extrude(outer_flange_height)
)
combined = base_solid.union(rib_solid)
# Chamfer outer edges
combined = combined.edges().chamfer(chamfer_distance)
# Fillet inner transition edges
combined = combined.edges().fillet(fillet_radius)
# Counterbore on central face
combined = (
    combined
    .faces(">Z")
    .workplane()
    .cskHole(pilot_hole_diameter, counterbore_diameter, counterbore_depth)
)
# Mounting holes pattern on top face
mount_radius = outer_radius - mount_hole_setback
mount_points = []
for i in range(num_mount_holes):
    angle = math.radians(i * 360.0 / num_mount_holes)
    x = mount_radius * math.cos(angle)
    y = mount_radius * math.sin(angle)
    mount_points.append((x, y))
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)
result = combined