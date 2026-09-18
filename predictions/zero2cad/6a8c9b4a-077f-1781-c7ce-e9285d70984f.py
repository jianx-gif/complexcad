import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 40.0
ring_height = 20.0
wall_thickness = 4.0
rib_width = 6.0
rib_height = 12.0
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = 30.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

base = cq.Workplane("XY").circle(outer_radius).extrude(ring_height)
spacer = base.shell(wall_thickness)
spacer = spacer.edges().chamfer(chamfer_size)

rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_width / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(ring_height)
)

ribs = rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

spacer = spacer.union(ribs)

hole_positions = []
for i in range(mount_hole_count):
    angle = i * 360.0 / mount_hole_count
    x = mount_hole_radius * math.cos(math.radians(angle))
    y = mount_hole_radius * math.sin(math.radians(angle))
    hole_positions.append((x, y))

spacer = (
    spacer
    .workplane(offset=ring_height / 2.0)
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

result = spacer