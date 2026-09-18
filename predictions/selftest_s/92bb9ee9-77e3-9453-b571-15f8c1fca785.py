import cadquery as cq
import math

cap_outer_radius = 45.0
cap_height = 30.0
wall_thickness = 5.0
rib_height = 5.0
rib_thickness = 2.0
rib_base_height = 10.0
top_chamfer = 2.0
base_chamfer = 0.5
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_offset = 5.0

inner_radius = cap_outer_radius - wall_thickness
rib_outer_radius = inner_radius + rib_thickness

profile_wp = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, rib_base_height)
    .lineTo(inner_radius, rib_base_height)
    .lineTo(inner_radius, rib_base_height + rib_height)
    .lineTo(rib_outer_radius, rib_base_height + rib_height)
    .lineTo(rib_outer_radius, rib_base_height)
    .lineTo(inner_radius, rib_base_height)
    .lineTo(inner_radius, cap_height - top_chamfer)
    .lineTo(cap_outer_radius, cap_height - top_chamfer)
    .lineTo(cap_outer_radius, cap_height)
    .lineTo(0, cap_height)
    .close()
)

cap = (
    profile_wp
    .revolve(360)
    .edges("<Z")
    .chamfer(base_chamfer)
)

offset = cap_height - top_chamfer
wedge = (
    cq.Workplane("XY")
    .box(cap_outer_radius * 2, top_chamfer * 2, top_chamfer * 2)
    .translate((0, 0, offset))
    .rotate((0, 0, 0), (0, 1, 0), 45)
)

cap = cap.cut(wedge)

hole_positions = [
    (mount_hole_spacing / 2, cap_height - mount_hole_offset),
    (-mount_hole_spacing / 2, cap_height - mount_hole_offset)
]

for x, _z in hole_positions:
    cap = cap.faces(">Z").workplane().center(x, 0).hole(mount_hole_diameter)

result = cap