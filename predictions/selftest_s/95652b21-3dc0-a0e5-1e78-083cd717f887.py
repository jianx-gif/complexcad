import cadquery as cq
import math

outer_radius = 50.0
hub_radius = 12.0
disc_thickness = 8.0
central_hole_diameter = 6.0
vent_ring_count = 3
vent_ring_width = 3.0
vent_ring_spacing = 5.0
mount_hole_diameter = 4.0
mount_hole_count = 8
mount_hole_radius = outer_radius - 5.0
chamfer_size = 0.8

profile_points = [
    (0, 0),
    (hub_radius, 0),
    (hub_radius, disc_thickness),
    (outer_radius, disc_thickness),
    (outer_radius, 0),
]
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve()
)
central_hole = (
    cq.Workplane("XY")
    .circle(central_hole_diameter / 2)
    .extrude(-disc_thickness)
)
result = result.cut(central_hole)
for i in range(vent_ring_count):
    inner = hub_radius + (i + 1) * vent_ring_spacing
    outer = inner + vent_ring_width
    outer_cyl = cq.Workplane("XY").circle(outer).extrude(-disc_thickness)
    inner_cyl = cq.Workplane("XY").circle(inner).extrude(-disc_thickness)
    result = result.cut(outer_cyl).union(inner_cyl)
mount_hole = cq.Workplane("XY").circle(mount_hole_diameter / 2).extrude(-disc_thickness)
for idx in range(mount_hole_count):
    angle = idx * 360.0 / mount_hole_count
    x = mount_hole_radius * math.cos(math.radians(angle))
    y = mount_hole_radius * math.sin(math.radians(angle))
    hole = mount_hole.translate((x, y, 0))
    result = result.cut(hole)
result = result.edges().chamfer(chamfer_size)
