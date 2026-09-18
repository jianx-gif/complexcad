import cadquery as cq
import math

# Parameter definitions
outer_diameter = 80.0
inner_diameter = 30.0
plate_thickness = 8.0
pocket_depth = 4.0
pocket_outer_radius = 12.0
pocket_inner_radius = 6.0
chamfer_distance = 2.0
mount_hole_dia = 6.0
mount_hole_offset = 25.0
num_mount_holes = 4
rib_width = 3.0
rib_angle = 30.0

half_thick = plate_thickness / 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# Base washer by revolving a composite sketch
washer = (
    cq.Workplane('XZ')
    .moveTo(outer_radius, -half_thick)
    .lineTo(outer_radius, half_thick)
    .lineTo(inner_radius, half_thick)
    .lineTo(inner_radius, -half_thick)
    .close()
    .revolve(360)
)

# Central milled pocket (two-step radius)
outer_pocket = (
    cq.Workplane('XY')
    .center(0, 0)
    .circle(pocket_outer_radius)
    .extrude(-pocket_depth)
)
inner_pocket = (
    cq.Workplane('XY')
    .center(0, 0)
    .circle(pocket_inner_radius)
    .extrude(-pocket_depth)
)
washer = washer.cut(outer_pocket).cut(inner_pocket)

# Mounting holes around inner diameter
angle_step = 360.0 / num_mount_holes
hole_positions = [
    (
        mount_hole_offset * math.cos(math.radians(i * angle_step)),
        mount_hole_offset * math.sin(math.radians(i * angle_step))
    )
    for i in range(num_mount_holes)
]
washer = washer.faces('>Z').workplane().pushPoints(hole_positions).hole(mount_hole_dia)

# Outer chamfer on top and bottom edges
washer = washer.edges('>Z').chamfer(chamfer_distance)

# Reinforcing rib on inner rim (sector shape)
rib_profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius, -half_thick)
    .lineTo(inner_radius + rib_width, -half_thick)
    .lineTo(inner_radius + rib_width, half_thick)
    .lineTo(inner_radius, half_thick)
    .close()
)
rib = rib_profile.revolve(rib_angle)
washer = washer.union(rib)

result = washer