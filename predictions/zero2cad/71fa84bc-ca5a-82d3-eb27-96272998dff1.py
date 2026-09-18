import cadquery as cq
import math

plate_length = 100.0
plate_width = 80.0
plate_thickness = 5.0
rib_width = 10.0
rib_height = 3.0
central_hole_diameter = 20.0
countersink_hole_diameter = 5.0
countersink_diameter = 12.0
countersink_angle = 82.0
countersink_count = 8
countersink_radius = 30.0
chamfer_size = 1.0

base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)

rib = (
    cq.Workplane('XY')
    .rect(plate_length, plate_width)
    .extrude(rib_height)
    .faces('>Z')
    .workplane()
    .rect(plate_length - 2 * rib_width, plate_width - 2 * rib_width)
    .cutBlind(-rib_height)
    .translate((0, 0, plate_thickness))
)

result = base.union(rib)

result = result.faces('>Z').workplane().hole(central_hole_diameter)

points = []
for i in range(countersink_count):
    angle = 2 * math.pi * i / countersink_count
    x = countersink_radius * math.cos(angle)
    y = countersink_radius * math.sin(angle)
    points.append((x, y))

result = result.faces('>Z').workplane().pushPoints(points).cskHole(countersink_hole_diameter, countersink_diameter, countersink_angle)

result = result.edges('|Z').chamfer(chamfer_size)
