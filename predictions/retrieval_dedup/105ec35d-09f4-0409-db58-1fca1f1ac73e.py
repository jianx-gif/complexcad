import cadquery as cq
import math

leg_length = 80.0
leg_width = 30.0
thickness = 8.0
clearance_hole_dia = 6.0
mount_hole_offset = 10.0
rib_thickness = 4.0
rib_height = 4.0
rib_spacing = 20.0
boss_dia = 12.0
boss_height = 6.0
chamfer_angle = 30.0
chamfer_dist = 2.0  # reduced to ensure manufacturability

points = [
    (0, 0),
    (leg_width, 0),
    (leg_width, leg_length - leg_width),
    (leg_length, leg_length - leg_width),
    (leg_length, leg_length),
    (0, leg_length),
]

base = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

base = base.edges().chamfer(chamfer_dist)

rib_centers = []
num_ribs = int((leg_length - leg_width) / rib_spacing)
for i in range(num_ribs):
    y = leg_width / 2 + i * rib_spacing + rib_spacing / 2
    if y < leg_length - leg_width / 2:
        rib_centers.append((leg_width / 2, y))

ribs = (
    base.faces(">Z")
    .workplane()
    .pushPoints(rib_centers)
    .rect(rib_thickness, rib_height)
    .extrude(rib_height)
)

boss_center_x = leg_width
boss_center_y = leg_length - leg_width
boss = (
    base.faces(">Z")
    .workplane()
    .center(boss_center_x, boss_center_y)
    .circle(boss_dia / 2)
    .extrude(boss_height)
)

combined = base.union(ribs).union(boss)

hole_positions = [
    (leg_width / 2, mount_hole_offset),
    (leg_width / 2, leg_length - mount_hole_offset),
    (mount_hole_offset, leg_width / 2),
    (leg_length - mount_hole_offset, leg_width / 2),
]

result = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(clearance_hole_dia)
)
