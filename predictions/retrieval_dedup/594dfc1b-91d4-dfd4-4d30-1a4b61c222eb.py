import cadquery as cq
import math
cover_height = 60.0
base_height = 20.0
wall_thickness = 5.0
base_radius = 40.0
front_radius = 25.0
num_slots = 8
slot_width = 12.0
slot_depth = 8.0
fillet_radius = 0.5
mount_hole_dia = 6.0
mount_hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_height)
)
mid_height = cover_height - base_height
# lofted dome
dome = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(base_radius)
    .workplane(offset=mid_height)
    .circle(front_radius)
    .loft()
)
solid = base.union(dome)
# thin wall
hollow = solid.shell(-wall_thickness)
# fillet outer bottom edge for safety
hollow = hollow.edges().fillet(fillet_radius)
# mounting holes on bottom face
hole_positions = []
for i in range(4):
    angle = math.radians(i * 90)
    r = base_radius - mount_hole_offset
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    hole_positions.append((x, y))
hollow = (
    hollow.faces("<Z").workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_dia)
)
# ventilation slots on top face
slot_center_radius = front_radius - slot_depth / 2.0
result = (
    hollow.faces(">Z").workplane()
    .center(slot_center_radius, 0)
    .slot2D(slot_width, slot_depth)
    .polarArray(radius=slot_center_radius, startAngle=0, angle=360, count=num_slots)
    .cutThruAll()
)
