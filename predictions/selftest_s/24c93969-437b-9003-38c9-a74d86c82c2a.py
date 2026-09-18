import cadquery as cq
import math
outer_diameter = 80.0
plate_thickness = 8.0
slot_width = 5.0
slot_length = 20.0
slot_count = 10
slot_radius = outer_diameter/2 - slot_length/2
angle_step = 360.0/slot_count
slot_points = []
for i in range(slot_count):
    theta = math.radians(i*angle_step)
    slot_points.append((slot_radius*math.cos(theta), slot_radius*math.sin(theta)))
plate = (
    cq.Workplane('XY')
    .circle(outer_diameter/2)
    .extrude(plate_thickness)
)
slots = (
    cq.Workplane('XY')
    .pushPoints(slot_points)
    .rect(slot_width, slot_length)
    .extrude(plate_thickness)
)
result = plate.cut(slots)