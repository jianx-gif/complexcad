import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 30.0
thickness = 8.0
slot_width = 5.0
slot_length = 20.0
slot_count = 12
slot_radius = (outer_diameter/2 + inner_diameter/2)/2
chamfer_distance = 1.0
rib_width = 4.0
rib_height = 2.0
rib_count = 6
rib_radius = inner_diameter/2 + 5.0

base = (
    cq.Workplane("XY")
    .sketch()
    .circle(outer_diameter/2)
    .circle(inner_diameter/2)
    .finalize()
    .extrude(thickness)
)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)

ribs = rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(rib.rotate((0,0,0), (0,0,1), angle))

base = base.union(ribs)

slot = (
    cq.Workplane("XY")
    .rect(slot_width, slot_length)
    .extrude(thickness + 2)
)

slots = slot
for i in range(1, slot_count):
    angle = i * 360.0 / slot_count
    slots = slots.union(slot.rotate((0,0,0), (0,0,1), angle))

slots = slots.translate((slot_radius, 0, -1))

base = base.cut(slots)

result = base.edges("|Z").chamfer(chamfer_distance)
