import cadquery as cq
import math

plate_width = 80.0
plate_length = 100.0
plate_thickness = 8.0
boss_diameter = 30.0
boss_height = 5.0
hole_diameter = 5.0
hole_depth = 6.0
hole_radius = 20.0
chamfer_size = 0.8
rib_thickness = 4.0
rib_height = 3.0
rib_spacing = 20.0

base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_length)
    .extrude(plate_thickness)
)

boss = (
    base.faces(">Z").workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

hole_positions = [
    (hole_radius * math.cos(math.radians(a)), hole_radius * math.sin(math.radians(a)))
    for a in (0, 120, 240)
]

with_holes = (
    boss.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, depth=hole_depth)
)

rib_count = int((plate_width - rib_thickness) // rib_spacing) + 1
rib_start = -plate_width / 2 + rib_thickness / 2
rib_positions = [rib_start + i * rib_spacing for i in range(rib_count)]

ribs = (
    with_holes.faces("<Z").workplane()
    .pushPoints([(x, 0) for x in rib_positions])
    .rect(rib_thickness, plate_length)
    .extrude(rib_height)
)

result = (
    ribs.faces(">Z").edges()
    .chamfer(chamfer_size)
)
