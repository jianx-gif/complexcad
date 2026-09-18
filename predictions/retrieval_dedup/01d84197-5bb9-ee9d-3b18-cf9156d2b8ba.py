import cadquery as cq
import math

outer_radius = 40.0
inner_radius = 10.0
initial_thickness = 20.0
wall_thickness = 5.0
chamfer_distance = 2.0
slot_width = 5.0
slot_length = 10.0
slot_count = 8
slot_radius_offset = outer_radius - slot_length/2 - 1.0
boss_radius = 6.0
boss_height = 4.0
fastener_hole_diameter = 4.0
fastener_hole_count = 6
fastener_hole_radius = inner_radius - 2.0

outer = cq.Workplane("XY").circle(outer_radius).extrude(initial_thickness)
inner = cq.Workplane("XY").circle(inner_radius).extrude(initial_thickness)
base = outer.cut(inner)
base = base.faces(">Z").edges().chamfer(chamfer_distance)
washer = base.shell(wall_thickness)
for i in range(slot_count):
    angle = 360.0 / slot_count * i
    washer = (
        washer.faces(">Z")
        .workplane()
        .center(slot_radius_offset, 0)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .rect(slot_width, slot_length)
        .cutBlind(-wall_thickness)
    )
# Create central boss and union
boss = cq.Workplane("XY").center(0, 0).circle(boss_radius).extrude(boss_height)
washer = washer.union(boss)
fastener_points = []
angle_step = 360.0 / fastener_hole_count
for i in range(fastener_hole_count):
    a = math.radians(i * angle_step)
    x = fastener_hole_radius * math.cos(a)
    y = fastener_hole_radius * math.sin(a)
    fastener_points.append((x, y))
washer = (
    washer.faces(">Z")
    .workplane()
    .pushPoints(fastener_points)
    .hole(fastener_hole_diameter)
)
result = washer
