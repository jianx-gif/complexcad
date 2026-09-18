import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 30.0
plate_thickness = 8.0
rib_height = 3.0
rib_width = 5.0
chamfer_distance = 2.0
mount_hole_diameter = 8.0
mount_hole_offset = 25.0
slot_width = 4.0
slot_length = 12.0
slot_count = 6
slot_radius = 20.0
boss_height = 2.0
boss_diameter = inner_diameter - 4.0

base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(plate_thickness)
)

rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2 + rib_width)
    .circle(outer_diameter / 2)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)

result = base.union(rib)

result = result.faces(">Z").edges().chamfer(chamfer_distance)

mount_points = [
    (mount_hole_offset, 0),
    (-mount_hole_offset, 0),
    (0, mount_hole_offset),
    (0, -mount_hole_offset),
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

slot_angles = [i * 360.0 / slot_count for i in range(slot_count)]
slot_points = [
    (
        slot_radius * math.cos(math.radians(a)),
        slot_radius * math.sin(math.radians(a)),
    )
    for a in slot_angles
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(slot_points)
    .rect(slot_width, slot_length)
    .cutBlind(- (plate_thickness + rib_height))
)

boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((0, 0, -boss_height))
)
result = result.union(boss)
