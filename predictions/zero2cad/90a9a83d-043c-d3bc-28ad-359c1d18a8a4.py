import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 30.0
thickness = 12.0
groove_width = 4.0
groove_depth = 2.0
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = 35.0
rib_width = 6.0
rib_height = 3.0
rib_count = 6

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
groove_outer_radius = inner_radius + groove_width

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

groove = (
    cq.Workplane("XY")
    .circle(groove_outer_radius)
    .circle(inner_radius)
    .extrude(groove_depth)
    .translate((0, 0, thickness / 2.0 - groove_depth / 2.0))
)

result = base.cut(groove)

hole_positions = []
for i in range(mount_hole_count):
    angle = i * 360.0 / mount_hole_count
    x = mount_hole_radius * math.cos(math.radians(angle))
    y = mount_hole_radius * math.sin(math.radians(angle))
    hole_positions.append((x, y))

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
    .translate((outer_radius - rib_width / 2.0, 0, 0))
)

ribs = rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = result.union(ribs)

result = result.faces(">Z").edges().chamfer(chamfer_size)
