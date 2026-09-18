import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 30.0
plate_thickness = 8.0
chamfer_distance = 2.0
mount_hole_diameter = 6.0
mount_hole_offset = 25.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_count = 4
rib_angle_step = 360.0 / rib_count

base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(plate_thickness)
)

mount_points = [
    (mount_hole_offset, 0),
    (-mount_hole_offset, 0),
    (0, mount_hole_offset),
    (0, -mount_hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

base = base.faces(">Z").edges().chamfer(chamfer_distance)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

ribs = cq.Workplane("XY")
for i in range(rib_count):
    angle = i * rib_angle_step
    x = (inner_diameter / 2 + rib_thickness / 2) * math.cos(math.radians(angle))
    y = (inner_diameter / 2 + rib_thickness / 2) * math.sin(math.radians(angle))
    ribs = ribs.union(rib.translate((x, y, plate_thickness / 2)))

result = base.union(ribs)
