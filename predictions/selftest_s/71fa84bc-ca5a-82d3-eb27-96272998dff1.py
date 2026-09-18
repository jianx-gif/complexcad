
import cadquery as cq
import math

plate_length = 100.0
plate_width = 80.0
plate_thickness = 5.0
rib_height = 8.0
rib_inner_offset = 10.0
central_hole_diameter = 20.0
screw_diameter = 5.0
screw_head_diameter = 10.0
countersink_angle = 82.0
screw_count = 8
screw_circle_radius = 30.0
chamfer_size = 1.0
slot_width = 8.0
slot_length = 30.0

base = (
    cq.Workplane('XY')
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

rib = (
    cq.Workplane('XY')
    .rect(plate_length, plate_width)
    .extrude(rib_height)
    .cut(
        cq.Workplane('XY')
        .rect(plate_length - 2 * rib_inner_offset, plate_width - 2 * rib_inner_offset)
        .extrude(rib_height)
    )
)

assembly = base.union(rib)

assembly = (
    assembly
    .faces('>Z')
    .workplane()
    .hole(central_hole_diameter)
)

angles = [2 * math.pi * i / screw_count for i in range(screw_count)]
points = [(screw_circle_radius * math.cos(a), screw_circle_radius * math.sin(a)) for a in angles]
assembly = (
    assembly
    .faces('>Z')
    .workplane()
    .pushPoints(points)
    .cskHole(
        screw_diameter,
        plate_thickness + rib_height,
        countersink_angle,
        screw_head_diameter
    )
)

assembly = (
    assembly
    .faces('>Z')
    .workplane()
    .center(plate_length / 2 - slot_length / 2, 0)
    .rect(slot_length, slot_width)
    .cutBlind(plate_thickness + rib_height)
)

result = (
    assembly
    .edges('|Z')
    .chamfer(chamfer_size)
)
